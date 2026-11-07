# Plan: Update NSF EAGER Concept Outline Based on FLAIME Genesis Mission Work (PR #58)

> **Context:** The EAGER thread (this PR) was paused so the PI could focus 100% on the FLAIME
> Genesis Mission proposal (DE-FOA-0003612, Topic 3-B), now consolidated in PR #58
> (`consolidation-2` branch, `genesis-mission-proposal/`). Intent is to revive the EAGER
> submission with everything the Genesis Mission effort produced — real preliminary data,
> signed partner letters, working benchmarks, and a sharper scientific narrative — while
> keeping the EAGER's narrower scope (VLM integration as a single testable hypothesis).
>
> **EAGER vs. Genesis (do not conflate):**
>
> | Dimension          | EAGER (this concept)                                     | FLAIME Genesis Mission (PR #58)                          |
> | ------------------ | -------------------------------------------------------- | -------------------------------------------------------- |
> | Sponsor            | NSF CMMI Advanced Manufacturing                          | DOE Genesis Mission (AMMTO/CMEI), Topic 3-B              |
> | Budget             | ~$300K                                                   | $750K total ($600K BYU + ~$150K partners)                |
> | Duration           | 2 years                                                  | 9 months Phase I (Jul 2026 → Mar 2027)                   |
> | Page limit         | 8 pp Project Description (Concept Outline 1–2 pp first)  | 5 pp Project Narrative                                   |
> | Central hypothesis | *Can a VLM with electrified trays integrate diverse instruments as a lab backbone?* | *FLAIME closed-loop pipeline discovers Al alloys at scale via pKGFN BOFN over multi-fidelity CALPHAD + atomization + LPBF + characterization.* |
> | Scope              | VLM hardware integration proof-of-concept; alloy discovery deferred | Full closed-loop discovery campaign with 15-element Al palette |
> | Reviewer audience  | Linkan Bian / Satish Bukkapatnam (CMMI AM)               | DOE merit panel + program officer synthesis              |

---

## 1. What FLAIME Generated That the EAGER Should Pull In

These are the assets created during PR #58 that materially strengthen the EAGER case
(grouped by what they unlock in the EAGER narrative).

### 1.1 Real preliminary experimental data (now in hand)

- **SEM/EDS images** of precursor powders + AMAZEMET-atomized custom mixture
  (Genesis Fig. 2 right panels) — directly evidences operator-assisted atomization
  feasibility, which the EAGER currently only *plans* to demonstrate.
- **Tensile data** on AlSi10Mg printed by U. Utah (Spear) and 3D Powder Tech
  (Genesis Fig. 4) — evidences that the LPBF→characterization handoff already works
  manually, and the EAGER's job is to automate it via VLM tray transport.
- **pKGFN benchmark results** (`benchmarks/figures/pkgfn_convergence.png`,
  `pkgfn_cost_efficiency.png`, `pkgfn_node_selection.png`) — already-published
  evidence the closed-loop optimizer functions, removing the "vaporware optimizer"
  reviewer concern.
- **CALPHAD landscape** (`benchmarks/figures/calphad_landscape.png`) and the
  pycalphad >100 calcs/sec demo currently cited only by reference.

**EAGER action:** Add a "Preliminary Results" subsection (½ page) citing these
figures. Frame as: "The scientific pipeline is *technically* working manually;
the EAGER de-risks the *hardware backbone* that makes it autonomous and replicable."

### 1.2 Signed partner letters (Genesis appendix-7-letters/)

Available in PR #58, all should be cross-referenced in the EAGER outreach steps
and concept outline:

| Letter                                          | Role for EAGER                                                  |
| ----------------------------------------------- | --------------------------------------------------------------- |
| `ashley-spear-uofu-loc.pdf`                     | LPBF access at U. Utah (validates EAGER's no-cost LPBF claim until BYU MX-100 commissioned) |
| `alik-nielsen-uofu-loc.pdf`                     | Spear-group student support                                     |
| `brian-jensen-byu-loc.pdf`                      | BYU internal collaborator (replaces / complements Crane/Homer/Killpack mock letters) |
| `thermo-calc-letter-of-collaboration.pdf`       | Thermo-Calc AB unfunded collaboration — validates TCAL8/TCAL10 license budget line |
| `meta-letter-of-collaboration.pdf`              | BoTorch tutorial integration — strengthens broader-impacts software-dissemination claim |
| `funded-subrecipients/` (Valimet, AMAZEMET)     | Atomization partners — Valimet for gas atomization at scale, AMAZEMET for ultrasonic atomizer |
| `distributed-validation-network/`               | Distributed-LPBF validation — directly maps to EAGER cloud-user-facility framing |

**EAGER action:** Replace the "mock letters available" stub with a
**placeholder-letters table** (PI directive: none signed today; use real
text in the placeholders following the PAPPG 2-sentence template). Carry
forward only those whose scope makes sense at $300K / 2-yr / VLM focus:

- **Spear (U. Utah) LPBF access** — included; PI confirmed it is OK to
  cite in the EAGER too (placeholder letter, not a Genesis-exclusive
  artifact).
- **Jensen (BYU)** — included as placeholder.
- **Thermo-Calc** — included as placeholder (unfunded collaboration,
  validates TCAL8/TCAL10 license budget line).
- **Kardex Remstar** — *new* placeholder letter to pursue **before**
  Concept Outline submission (PI directive; see §4).
- **AMAZEMET** — *deferred*. PI directive: do not name AMAZEMET as an
  EAGER partner; the Genesis letter scope is Genesis-only. Reference the
  ultrasonic atomizer generically as "vendor-provided ultrasonic
  atomization (~$220K, PI startup)" with no named-partner letter.
- **Valimet, Meta** — defer (Genesis-only relevance at this scope).

### 1.3 Sharpened scientific framing

- **Hierarchical search-space architecture** (pop. plan §"Hierarchical Search
  Space Architecture"): 15-element Al palette → NChooseK selection → multi-fidelity
  CALPHAD (pycalphad → TC-Python/TCAL10 → AM Module). The EAGER should still
  *narrow* this — pick a single sub-system (e.g., Al-Mn-Cr-Zr-Mg-Si as Edison-graded
  best fit) and use the hierarchy as preliminary evidence the framework scales.
- **Mineral Burden Score (MBS)** as a domain-relevant objective — gives the EAGER a
  more compelling "why aluminum, why these elements" story than the current
  AlSi10Mg-only framing.
- **"Frugal twin" + SDL leadership** positioning (PI directives D1, D4, D5):
  PI is lead author on the SDL-for-structural-materials review section; this is
  stronger NSF intellectual-merit framing than the current outline provides.
- **Honegumi + BoTorch tutorials** as concrete broader-impact deliverables (D2)
  with the Meta letter as evidence — currently the EAGER broader impacts are
  generic. Replace with: "Open-source VLM orchestration plug-ins for Honegumi
  + worked BoTorch tutorials demonstrating BOFN-on-instruments."

### 1.4 Personnel & budget realism

- FLAIME audit (memory: "FLAIME Phase I budget") established credible BYU
  personnel rates: [PI rate removed], MS @ $24K/9-mo full-time,
  UG @ $12K/student/yr (20 hr × 15 wk × 2 sem × $20/hr).
- BYU fringe rate for faculty summer salary is **19.7%** (not the 51.1% staff
  rate); the EAGER should use 19.7% on PI summer wages.
- 51.5% MTDC F&A confirmed; equipment ≥$5K excluded from MTDC base (MX-100,
  VLM both qualify).
- Travel @ $1,300/trip baseline.
- 4.5N argon (~$19K/2yr) line item from FLAIME budget should appear in EAGER
  M&S — it's a real recurring cost the current EAGER omits.

**EAGER action:** Re-cast the budget table using FLAIME-validated rates rather
than the current Edison-derived estimates. Most line items shift only modestly
but the *credibility* of the numbers improves substantially when the panel
checks against any BYU benchmark.

### 1.5 Compliance & DEI/safety language now battle-tested

- FLAIME `proposal-checklist.md` has a fully fleshed safety, foreign-connections,
  AI-tool-disclosure, DMSP, and broader-impacts skeleton. Most of this can be
  trimmed to NSF-PAPPG conventions (NSF doesn't have the same foreign-connections
  template DOE does, but Responsible Conduct of Research, Single-Copy Documents,
  and Postdoc Mentoring Plans should be addressed).
- Safety/EHS section (Genesis appendix) covers Class 4 laser interlocks,
  NFPA 484 powder, O₂ monitoring, Class D suppression — all already requested
  by Edison Review v2 of the EAGER.

---

## 2. What to **Keep Narrow** in the EAGER (Do Not Inherit from FLAIME)

EAGER review hinges on a single high-risk hypothesis. Resist the urge to import
the full FLAIME pipeline — the panel will (correctly) ask "why isn't this a
standard CMMI proposal?". Items to **explicitly defer** in the EAGER:

1. **15-element Al palette / NChooseK BO** — keep as 1-paragraph forward-looking
   reference; EAGER's experimental scope stays at AlSi10Mg + 1 custom composition.
2. **22,803-sub-system CALPHAD enumeration** — cite as preliminary computational
   evidence (Year-1 deliverable) but do not commit to it as a Year-2 milestone.
3. **Distributed-LPBF validation network** — defer; mention only as Year-2
   stretch goal once VLM integration is validated.
4. **Cloud user-facility model** — already deferred per Edison review v2; keep
   it deferred.
5. **Industry cost-share / 20% industry funding cap** — Genesis-only constraint;
   irrelevant for NSF EAGER.
6. **9-month go/no-go gate** — Genesis-specific; EAGER uses 2-yr internal review.

---

## 3. Concrete Edit Plan for `eager-concept-outline.{md,tex}`

Below is the section-by-section diff plan. Each item is an independent edit;
apply in any order.

### §0 Title block / front matter

- [ ] Rename concept to **FLAIME-VCL** (per PI decision in §6). Keep
      "Vertical Cloud Laboratory" as the spelled-out long form on first use
      so NSF reviewers — who have not seen FLAIME — get the descriptive
      anchor. Subsequent references use "FLAIME-VCL" and one-line keyword
      "(VCL hardware backbone of the FLAIME closed-loop pipeline)".
- [ ] Replace the "BYU internal collaborators with letters of collaboration:
      Crane, Homer, Killpack" stub with **placeholder letters that contain
      real text** (PI directive — none are signed today). Use the
      PAPPG-compliant 2-sentence Letter of Collaboration template from
      `genesis-mission-proposal/.../appendix-7-letters/` as the model;
      mark filenames with a `-placeholder` suffix so the signed-vs-draft
      distinction stays visible in repo. Jensen letter from Genesis is
      also still a placeholder for EAGER purposes (do not assume signed).

### §1 Problem framing

- [ ] Add 1 sentence on critical-minerals motivation (MBS framing, supply-risk
      span Fe → Sc) — frames why VLM-enabled discovery matters for an Al-alloy
      portfolio, not just LPBF parameter optimization.
- [ ] Update competitive-landscape paragraph: keep APEX/AMASE/Cooper/A-Lab
      table; add explicit statement that **none of these use a VLM** (verified
      via Edison v2's VLM-taxonomy citation, Muñoz 2025).

### §2 Hypothesis & scope (KEEP NARROW)

- [ ] No change to the single-hypothesis statement.
- [ ] Update the "3–5 integrated instruments" target to name them concretely
      based on what is now realistically procurable:
      OT-2, AutoTrickler V4, ultrasonic atomizer (startup), MX-100, optical
      microscope, hardness tester. (6 instruments, exceeds the original 3–5
      floor.)

### §3 Approach / preliminary evidence  *(NEW SUBSECTION)*

- [ ] Add ½-page "Preliminary Evidence" subsection citing:
  - pKGFN benchmark results (cost-aware screening, cite figure)
  - SEM/EDS of AMAZEMET-atomized custom Al composition
  - AlSi10Mg tensile data from Spear-group prints
  - pycalphad >100 calcs/sec demo
- [ ] Cross-reference `benchmarks/` and `genesis-mission-proposal/figures/`
      paths so reviewers can audit the underlying artifacts on request
      (NSF allows this even though external URLs are discouraged).

### §4 Go/no-go milestones (Edison v2 revisions)

- [ ] Increase autonomous-cycle milestone from ≥5 → **≥20** (Edison v2
      recommendation; FLAIME uses higher numbers, EAGER should at least bump).
- [ ] Add explicit definition of "autonomous" (no human in instrument-loop
      between print kickoff and characterization-data export).
- [ ] Keep the other 3 milestones (positioning, vibration, 24-hr operation).

### §5 Safety / EHS (Edison v2 revisions)

- [ ] Add: O₂ monitoring inside VLM tray volume during atomizer/LPBF operation.
- [ ] Add: Class D fire suppression in VLM enclosure (Al fines are Class D
      combustible).
- [ ] Add: Powder containment during tray transport (sealed cassettes,
      validated by AMAZEMET partner).
- [ ] Cite NFPA 484 explicitly (already in current outline — keep).

### §6 Software / orchestration  *(NEW or expand existing line)*

- [ ] Name the orchestration approach: **Honegumi + Ax + custom VLM driver
      (open-source on GitHub under vertical-cloud-lab org)**.
- [ ] Cite Meta letter of collaboration for BoTorch-tutorial dissemination.
- [ ] Mention AlabOS (Berkeley A-Lab) and Bluesky (NSLS-II) as compared
      alternatives — explain why the EAGER builds its own thin VLM driver
      rather than adopting either wholesale.

### §7 Budget table

- [ ] Re-derive every line using FLAIME-validated unit costs (see §1.4 above).
- [ ] Add 4.5N argon line (~$10K/2yr, scaled down from FLAIME's $19K/9mo).
- [ ] Use 19.7% PI fringe (not staff rate).
- [ ] Verify VLM + MX-100 are each ≥$5K so they correctly drop out of MTDC
      base for F&A.
- [ ] Show MTDC subtotal explicitly so the panel can recompute F&A.

### §8 Outreach / `grant-targeting-analysis.md`

- [ ] Update §8 (NSF EAGER) to note: PI has now produced a 5-page Genesis
      Mission proposal applying the same scientific framework — this is
      *evidence of execution capability*, which strengthens the EAGER PO
      conversation. Suggested email line: "We've recently submitted a DOE
      Genesis Mission proposal demonstrating the broader pipeline; the EAGER
      derisks the VLM hardware backbone that the larger campaign assumes."
- [ ] Add cross-reference to `genesis-mission-proposal/flaime-genesis-proposal-clean.pdf`
      as appendable evidence on request.

### §9 References

- [ ] Pull reference list into `eager-references.bib` mirroring the
      FLAIME `edison-references.bib` style so future PRs can share the BibTeX
      file across both proposals.
- [ ] Add the 3 new high-impact references Edison v2 surfaced:
      Muñoz 2025 (VLM taxonomy), Hung 2024 (autonomous lab survey),
      Salazar-Villacis 2026 (ADePT framework).

---

## 4. Out-of-Scope Consideration: Kardex as Lead Institution

The PI's earlier comment (#4230783488) raised the possibility of Kardex (or a
reseller) acting as lead institution on a future Genesis Mission VLM proposal.
For the **EAGER** specifically:

- NSF EAGER eligibility is **PI-led at an IHE** (Brigham Young University).
  Kardex cannot be lead.
- Kardex *should* provide a placeholder letter of support — **PI directive
  (§6): pursue this before Concept Outline submission.** Useful at the
  Concept Outline stage to demonstrate VLM vendor engagement and to lock
  in pricing / lead-time assumptions in the budget narrative.
- Action: Add to the EAGER outreach steps: "Request placeholder letter
  of support from Kardex Remstar (or authorized US reseller) confirming
  pricing, lead time, and engineering-support availability for the
  proposed VLM. Target: signed before Concept Outline goes to Linkan
  Bian."

---

## 5. Suggested Sequencing (Target: ASAP per PI §6)

1. ~~Wait for FLAIME submission close-out~~ — done (deadline 2026-04-28
   already passed; FLAIME submitted).
2. ~~PI go-decision on EAGER revival~~ — confirmed via PI answers in §6
   ("ASAP" target).
3. **Kick off Kardex letter request in parallel with edits** (§4 — long
   lead time on vendor sign-off, do not block on it).
4. **One commit per major edit block above** (§3.1–§3.9), each small
   enough to review quickly.
5. **Run a third Edison mock review** after edits land to confirm Edison
   v2's minor revisions are all resolved.
6. **PO concurrence email to Linkan Bian** (per current outreach steps in
   `grant-targeting-analysis.md`) using the updated 1-pager — only after
   step 5; attach Kardex letter if it has landed, otherwise note "vendor
   letter forthcoming."

**Submission window:** EAGERs to NSF AM are accepted any time; the
Concept Outline → PO concurrence → full proposal pipeline typically takes
3–6 months. Per PI directive (§6), target ASAP — start the Concept
Outline email within the same week the §3 edits land.

---

## 6. Resolved Decisions (PI answers — 2026-05-02)

| Question | PI answer | Reflected in plan |
| --- | --- | --- |
| Branding: "Vertical Cloud Laboratory" vs. "FLAIME-VLM" vs. "FLAIME-VCL"? | **FLAIME-VCL** (long form on first use; FLAIME-VCL thereafter) | §3 §0 title block |
| Which BYU letters are signed today (Jensen, Crane, Homer, Killpack)? | **None — all placeholders, but with real text** (use PAPPG 2-sentence template; mark filenames `-placeholder`) | §1.2, §3 §0 |
| OK to cite Spear LPBF access in the EAGER? | **Yes**, but the letter is a placeholder | §1.2 |
| Include AMAZEMET as a named partner? | **No** — letter scope is Genesis-only; reference atomizer generically | §1.2 |
| Pursue Kardex letter of support before Concept Outline submission? | **Yes** | §4, §5 |
| Target submission window (which NSF FY)? | **ASAP** — start Concept Outline email same week §3 edits land | §5 |

---

*Plan generated 2026-05-02 in response to PR #9 comment 4364094549. No code
or proposal text changed in this commit — this file is the plan only. Apply
the section edits in §3 once the PI confirms direction.*
