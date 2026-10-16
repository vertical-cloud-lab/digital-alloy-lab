# What changed in the last 5–6 months (Apr–Oct 2026): Edison follow-up synthesis

*Prepared 2026-10-06 for PR #90 (AFOSR YIP white paper and companion
early-career proposals). Companion to `../external-evaluator-slate.md`,
`../../early-career-award-adaptation.md`, and
`../../afosr-yip-white-paper/`.*

## What was run

| File | Edison job | Task ID | Scope |
|---|---|---|---|
| [`01-methods-novelty.md`](01-methods-novelty.md) | LITERATURE_HIGH | `3e37e5aa-b9dc-4ede-ace5-dd20993e4668` | BOFN, multi-fidelity BO, autonomous metal-AM labs, LLM agents, and a check on the novelty claim |
| [`02-extreme-env-alloys.md`](02-extreme-env-alloys.md) | LITERATURE_HIGH | `bf148e03-9f78-415b-b30f-ae10a5995bbb` | RCCAs and Nb alloys by AM, Co/Re/Hf-lean superalloys, high-temperature Al |
| [`03-feedstock-hte.md`](03-feedstock-hte.md) | LITERATURE_HIGH | `60d47dd5-2b1c-407e-a086-39591978f49c` | Ultrasonic atomization, in-situ alloying, miniature testing, automated characterization |
| [`04-funding-policy-landscape.md`](04-funding-policy-landscape.md) | LITERATURE_HIGH | `8c6f3634-78ca-4eda-9558-a179d5ef007f` | AFOSR, DOE ECRP, Genesis Mission, NSF, DoD, critical minerals |
| [`05-precedent-novelty.md`](05-precedent-novelty.md) | PRECEDENT | `4e6cabdf-216c-4c24-8310-161e896aa58a` | Has anyone applied cost-aware, partial-evaluation BOFN to an alloy AM pipeline? |

All five were submitted 2026-10-06 19:03 UTC and finished with `success`
21–31 min later. Full verbose trajectories are in [`raw/`](raw/). The
submit/wait/fetch script is
[`edison_recent_developments.py`](edison_recent_developments.py).

**How this was checked.** Edison's literature tools search papers, not
grants.gov, so the funding facts in Section 1 come from the official NOFO and
BAA PDFs. 32 of the 36 key DOIs and arXiv IDs below were resolved against
doi.org: titles matched and the dates shown are the registered online dates.
The remaining 4 were rate-limited and are marked "unchecked". Numbers that
Edison quoted from papers (strengths, lifetimes, sphericity, and so on) were
not re-read from the full text unless noted. Check them before quoting.

---

## 1. Time-critical items (from official sources, not Edison)

Edison's funding answer (Q4) **missed both of these**. It predicted the FY27
YIP NOFO for "late Oct–Dec 2026" and reported "no changes to the Sayir
portfolio." Both statements are wrong.

### 1a. The FY27 AFOSR YIP white paper is due Fri 2026-10-09, 11:59 PM ET

NOFO **FA955026S0003** ([listing](https://simpler.grants.gov/opportunity/c342c01d-4f34-440f-8bb2-4bdd4d763df0),
[PDF](https://apply07.grants.gov/grantsws/rest/opportunity/att/download/354995)),
posted 2026-09-08; a Q&A document was posted 2026-09-24.

- **The white paper is mandatory** and is submitted through the
  [AFOSR Qualtrics portal](https://afosr.gov1.qualtrics.com/jfe/form/SV_eKuTqm9qezoDYep).
  From the NOFO, p. 21: *"If you have previously submitted a white paper to
  the PO and feedback was provided you are still REQUIRED to submit under this
  NOFO … No exceptions will be granted."* You may submit to more than one
  discipline if each submission says so. Proposals themselves are limited to
  one portfolio.
- **Format (p. 21):** 8.5×11 in, 1 in margins, **1.5-line spacing**, **Times
  New Roman or Garamond 12 pt**, **≤5 pages** (cover page, CV, and references
  excluded).
- **Content (pp. 21–22):** a cover page with the NOFO number, research topic or
  discipline area, and the PI's contact details; the proposed research and
  issues; **potential impact on DAF and DoW capabilities**; **potential team
  members and development plans**; and the technical approach (**hypothesis**,
  theories, concepts, approaches, data measurements, and analysis). The CV must
  list all publications and presentations.
- **Scoring (p. 40):** technical merit and relationship to DoW missions,
  weighted equally, using a "weight of scientific evidence" approach
  (EO 14303). A separate go/no-go screen covers EO 14303/14332 compliance.
- **Timeline:** white-paper feedback by 2026-11-06 → full proposals (invited
  only) on Grants.gov by **2026-12-04** → selections ~2027-04-26.
- **Eligibility and award:** PhD on or after 2019-04-01; US citizen,
  national, or permanent resident; $150K/yr × 3 yr; at least 37 awards.
- **Q&A posted 2026-09-24**
  ([PDF](https://files.simpler.grants.gov/opportunities/c342c01d-4f34-440f-8bb2-4bdd4d763df0/attachments/9cf2fa75-6fdf-4713-a203-3f849f3001af/FA955026S0003_Qs_and_As.pdf)):
  - Q14: *"No domestic or foreign collaborators, funded or non-funded, are
    allowed for this single investigator award."* This rules out the
    "unfunded AFRL collaboration" and "BYU + Spear LPBF collaboration" ideas in
    `early-career-award-adaptation.md` §2.3.
  - Q15: postdocs, graduate students, and undergraduates are allowed, so the
    white paper's "potential team members" means lab personnel.
  - Q17: government-owned facilities may be used if they are named in the
    proposal.
  - Q9: there is no minimum amount of preliminary data.
  - Q5: for questions of fit, contact the PO listed in the general BAA.
  - Q13: more than one white paper is allowed.

### 1b. Sayir's portfolio text excludes structural materials, and a new subtopic fits a reframed pitch

The current AFOSR BAA **FA955026S0001**
([listing](https://simpler.grants.gov/opportunity/de479d2e-aad1-466a-acc3-d5d11cf7918d);
posted 2026-06-04, Amendment 0001 dated 2026-08-21) rewrote §A.3.a
*Aerospace Materials for Extreme Environments*. Sayir is now listed as
**AFOSR/RESB**, `extreme.environment@us.af.mil`, (703) 696-7236. That
portfolio mailbox is what the BAA lists; it differs from the personal
address given earlier in this PR.

- **Exclusion:** *"proposals focused primarily on structural or organic
  materials, device engineering, systems integration, or exploring the physics
  of known condensed matter phenomena … are not a fit for this program."* The
  FY25 BAA said something similar ("does not focus on the synthesis or
  applications of structural materials"), so
  `early-career-award-adaptation.md` §2.1's description of this portfolio as
  "high-temperature structural materials" was inaccurate from the start.
- **The opening: the new "Materials Synthesis by Design" subtopic.** It asks for
  *"a predictive framework that quantitatively links a material's structure to
  its function … the fundamental mechanisms by which external stimuli—such as
  electric fields, **lasers, or acoustic waves**—can guide the formation of
  desired material structures,"* and says *"a critical requirement is the
  integration of **Uncertainty Quantification (UQ)** into all synthesis models
  … distinguish between controllable process parameters and inherent
  stochastic variations, ultimately providing a **predictive confidence level
  for achieving any target microstructure**."* LPBF is laser-driven, ultrasonic
  atomization is acoustic, and GP-based BOFN quantifies uncertainty by
  construction. Pitching **synthesis → microstructure with calibrated
  confidence** as the scientific objective, rather than tensile or creep
  performance of structural alloys, matches this language.
- **No metallic-materials portfolio:** the current BAA has none and does not
  list Tiley. The closest methodology-first alternative is **§A.2.c Dynamic
  Data and Information Processing** (DDDAS and physics-enhanced ML; Dr. Erik
  Blasch, `D2IP@us.af.mil`). §A.1.e Aerospace Composite Materials (also Sayir)
  says *"Metal-based materials, while not excluded, are not a priority."*

### 1c. Other funding items worth knowing

- **DOE Genesis Mission SBIR/STTR Phase I** (opened 2026-07-22, ~40 awards).
  Topics include *Designing Materials with Predictable Functionality* and
  *Achieving AI-Driven Autonomous Laboratories*. Universities can take part
  only as an STTR research partner (≥30% of the work) to a US small business.
  A broader Phase I call is expected "later this fall." Separately, Cornell,
  UT Austin, and PNNL announced Genesis Mission awards in July 2026. I did not
  check which solicitation those awards came from.
- **DOE ECRP FY27:** no NOFO yet. A March 2027 pre-application is still the
  planning assumption.
- **NSF:** Edison cites reporting on the NSF restructuring (71 divisions
  consolidated) and award terminations. Treat CAREER 2027 logistics, including
  program homes and deadlines, as uncertain until the next solicitation is
  posted.

---

## 2. Novelty-claim check (Q1, Q2, Q5)

The current white paper (after the cringe-filter rewrite, `e3ed7b1`) says:
*"The core methodological novelty is the first application, to our
knowledge, of this cost-aware method to a complex additive manufacturing
workflow for alloys."*

**Verdict (all three Edison answers agree):** no paper or preprint was found
that uses cost-aware, partial-evaluation BO of a function network to choose
which **step of a physical alloy AM workflow** to run next. A narrowly worded
claim therefore still holds. The broad wording is risky because both the
method and the physical pipeline have close precedents:

| Precedent (verified DOI / date) | What it does | Why it matters here |
|---|---|---|
| Taheri-Mousavi, …, Olson, Hart, *Adv. Mater.* [10.1002/adma.202509507](https://doi.org/10.1002/adma.202509507) (online **2025-10-02**; Edison mislabeled it Oct 2026) | CALPHAD/ICME-informed composition BO → **ultrasonically atomized** powder → LPBF → tensile (Al, 395 MPa aged) | The closest physical composition-to-property pipeline. It is not a costed, node-selecting loop. (Olson, a co-author, is a top letter-writer candidate in the evaluator slate.) |
| Talbot, Zou, Hattrick-Simpers et al., *npj Adv. Manuf.* [10.1038/s44334-026-00098-5](https://doi.org/10.1038/s44334-026-00098-5) (2026-06-23) | **ALPHA-AM**: CALPHAD-informed constrained-EI active learning over **six generations** of DED NiCoCr alloys, with hardness, cracking, and oxidation feedback | The strongest new competitor. It rules out a "first closed-loop AM alloy discovery" claim. It uses a single surrogate with no atomization, no LPBF, and no partial evaluations. |
| Liang, Kusne, Takeuchi, Zhao, Babu et al., ChemRxiv [10.26434/chemrxiv.15001156/v1](https://doi.org/10.26434/chemrxiv.15001156/v1) (2026-03-23) | Real-time autonomous metal AM (NIST AMASE / UTK ecosystem) | Rules out "first autonomous metal AM." Kusne appears in evaluator-slate §B and §D; he is now on a near-competitor paper. |
| Torresi & Friederich, *Digital Discovery* [10.1039/d5dd00572h](https://doi.org/10.1039/d5dd00572h) (2026) | Multi-stage (cascade) BO with resumable intermediate samples for self-driving labs | The closest new *method* analogue. Not metals, and uniform stage costs in the main experiments. |
| Alvi, Vela, …, Arróyave, *npj Comput. Mater.* [10.1038/s41524-026-01981-7](https://doi.org/10.1038/s41524-026-01981-7) (2026-02-04) | Cost-aware deep-GP batch BO across unequal-cost property queries for RHEAs | Cost-aware BO for RHEAs now exists, but in silico and over properties rather than process steps. |
| Hur & Lee, arXiv [2607.04508](https://doi.org/10.48550/arXiv.2607.04508) (Jul 2026) | Agentic metal-AM (DED) lab that would substitute hardness for tensile tests when uncertainty allows | Proposed, not demonstrated. Still makes "first cost-aware intermediate-vs-final measurement in metal AM" risky to claim. |
| Yoon, Buathong, …, Frazier, arXiv [2609.02126](https://doi.org/10.48550/arXiv.2609.02126) (Sep 2026) | The BOFN group's scalable composite-function BO for electron-microscopy inverse problems | The Frazier group now works on materials, so don't claim "structured BO is new to materials." |

**Suggested replacement sentence** (precise, and defensible on the literature found):

> To our knowledge, no prior work has used cost-aware, partial-evaluation
> Bayesian optimization of a function network to decide *which step* of a
> physical alloy additive manufacturing workflow (powder production, printing,
> microstructure, or property testing) to run next. Recent closed-loop AM
> alloy campaigns instead optimize composition with a single surrogate and a
> fixed set of measurements (Talbot et al. 2026).

Per the PRECEDENT answer, say "demonstrated" only for steps the preliminary
data actually execute. Otherwise, write "we propose".

---

## 3. Worth citing (verified DOIs; numbers as read by Edison)

**For the white paper (pick 2–4):**
- **Dodge et al., *Powders* 5, 25** [10.3390/powders5030025](https://doi.org/10.3390/powders5030025) (2026-07-16; U. Louisville, NASA/NSF funded). Ultrasonic atomization of the refractory HEA **TiZrNbHfTa**, verified from the Crossref abstract. Melting used **vacuum arc melting plus ultrasonic-plasma atomization**, not induction. Sphericity 0.90–0.93, porosity ≤0.24%, a BCC solid solution with minor monoclinic Ti oxide. No AM builds. *It shows the route works for RHEAs, and it confirms that the **plasma/arc** module (not the induction module on hand) is the enabling hardware. That is a clean DURIP justification.*
- **Brizes et al., NASA technical report** [10.64631/zcym1460](https://doi.org/10.64631/zcym1460) (2026-09-01). LPBF dispersion-strengthened low-density Nb alloy: per Edison, uncoated rupture life ~21 h at 1093 °C / 20.7 MPa (~10× C-103), and **oxidation, not creep, limits life**. A concrete performance gap to target. Companion catalog: [10.64631/LBIQ7959](https://doi.org/10.64631/LBIQ7959).
- **Talbot et al. 2026** (above). Cite it to position against the closest competitor rather than leave it for a reviewer to raise.
- **Chawla, Penumadu & Kalinin, *Commun. Mater.*** [10.1038/s43246-026-01294-8](https://doi.org/10.1038/s43246-026-01294-8) (2026-08-19). Combinatorial libraries plus automated nanoindentation with GP-guided, cost-aware selection. External support for the "cheap proxy test vs. full tensile test" hierarchy.
- **Campo, Hanisch & Agar, *MRS Bull.*** [10.1557/s43577-026-01181-0](https://doi.org/10.1557/s43577-026-01181-0) (2026-09-23). "A national AI strategy for materials readiness across energy and defense." Useful for the required DAF/DoW-impact section.

**For a full proposal:**
- Li et al., *Nat. Commun.* [10.1038/s41467-026-71926-7](https://doi.org/10.1038/s41467-026-71926-7) (2026-04-15). LPBF heat-resistant Al with 582 MPa at room temperature and 114 MPa at 400 °C. *Present the aluminum preliminary data as **platform commissioning** rather than an extreme-environment result.*
- Chen et al., *Prog. Addit. Manuf.* [10.1007/s40964-026-01834-1](https://doi.org/10.1007/s40964-026-01834-1) (2026-07-10). GRX-810 yttria window of 0.30–0.45 wt%, relevant to the Ni secondary system.
- Keller et al., *Prog. Addit. Manuf.* [10.1007/s40964-026-01728-2](https://doi.org/10.1007/s40964-026-01728-2) (2026-05-07). Review of Nb-alloy AM; ~1 at.% O can make Nb nearly brittle, so oxygen should be a tracked node.
- Atabay, Baker, McKeown & Voisin (LLNL), *Mater. Des.* [10.1016/j.matdes.2026.116623](https://doi.org/10.1016/j.matdes.2026.116623) (Sep 2026). Ultrasonically atomized Ni–W powders. LLNL also has ultrasonic atomization; McKeown appears in evaluator-slate §D.
- Bajaj et al., *Sustainability* [10.3390/su18041843](https://doi.org/10.3390/su18041843) (2026-02-11). AMAZEMET rePOWDER with sphericity 0.93; oxygen pickup flagged.
- Villapun et al. [10.1007/s40964-026-01939-7](https://doi.org/10.1007/s40964-026-01939-7) (multi-composition screening on a production LPBF machine), Giri et al. [10.1007/s10845-026-02861-z](https://doi.org/10.1007/s10845-026-02861-z) (photodiode porosity classification as a cheap test), Zha et al. HT-DABI [10.2139/ssrn.6169831](https://doi.org/10.2139/ssrn.6169831) (high-throughput creep, which could serve as an intermediate test), and Cao et al. PanLink [10.1038/s41598-026-73329-6](https://doi.org/10.1038/s41598-026-73329-6) (fast CALPHAD-to-LPBF coupling).
- Refractory CALPHAD and ML: Peterson et al. arXiv [2609.14925](https://doi.org/10.48550/arXiv.2609.14925); Omprakash et al. arXiv [2609.06627](https://doi.org/10.48550/arXiv.2609.06627) (DFT-informed pycalphad databases for Cr-Hf-Mo-Nb-Ta-Ti-V-W-Zr, with no liquid phase yet); Jiang et al. [10.1088/2515-7639/ae44d1](https://doi.org/10.1088/2515-7639/ae44d1) (multi-fidelity active learning for TaNbMoVW).

---

## 4. Competitors and awareness

- **The Arróyave / BIRDSHOT ecosystem is publishing quickly** (consistent with
  evaluator-slate §E): DataScribe (arXiv 2601.07966, Jan 2026); Islam et al.,
  RHEA performance-manufacturability co-optimization (SSRN 7549378, Jan 2026;
  DOI unchecked); Sinha et al., LLM-switched constrained multi-objective BO
  (arXiv [2609.19550](https://doi.org/10.48550/arXiv.2609.19550)); and
  Arróyave's *Digital Discovery* perspective, "Metallurgy-informed Bayesian
  optimization" ([10.1039/D6DD00251J](https://doi.org/10.1039/D6DD00251J)).
- **LLNL APEX:** an autonomous DED alloy lab, described in Mallia & Caputo
  ([10.69709/caic.2026.133382](https://doi.org/10.69709/caic.2026.133382),
  2026-08-31).
- **AlloyGen (Taheri-Mousavi & Ni):** multi-agent LLM framework driving
  Thermo-Calc for AM alloys
  ([10.21203/rs.3.rs-10329502/v1](https://doi.org/10.21203/rs.3.rs-10329502/v1),
  2026-08-04). Prior art for "LLM agents run the CALPHAD step."
- **NASA Glenn** is active on both the refractory and the BO-benchmark fronts
  (Brizes; Stuckner, [10.64631/zkvt6687](https://doi.org/10.64631/zkvt6687)).
- **Northwestern HT-DABI group** (Zha et al.): high-throughput creep screening.

## 5. Edison caveats found during spot-checks

- Q4 missed the FY27 YIP NOFO and the BAA rewrite (Section 1). Its timing
  guidance ("NOFO late Oct–Dec; white papers Jan–Feb") is **wrong**; ignore it.
- Wrong dates: Taheri-Mousavi *Adv. Mater.* was online **2025-10-02**, and
  Sojoodi et al.'s ultrasonic-plasma-atomization review was online
  **2025-10-28**. Edison labeled both "Oct 2026", which is the issue date.
  "Thapliyal et al. (Nov 2026)" is also likely an issue date.
- Edison flagged several items as "unobtainable", meaning it read only the
  metadata or abstract: Sowards, Kumaravel, Xiao, Islam, Jiang, Priyadarshini,
  Liang, and Arróyave (Digital Discovery). Treat those summaries as leads.
- Unchecked (rate-limited) DOIs: SSRN 7549378,
  [10.1002/adem.202502047](https://doi.org/10.1002/adem.202502047),
  [10.1016/j.matdes.2026.115679](https://doi.org/10.1016/j.matdes.2026.115679),
  and [10.21203/rs.3.rs-10513494/v1](https://doi.org/10.21203/rs.3.rs-10513494/v1).
- None of the PI's own papers appear among the recommendations.

## 6. Suggested next steps before 2026-10-09

1. **Today:** send a short fit-check email to `extreme.environment@us.af.mil`
   (subject line includes FA955026S0003). Pitch synthesis-by-design
   (laser/acoustic processing → target microstructure, with UQ) and ask whether
   refractory-alloy structural targets are in scope.
2. **Reformat the white paper to the NOFO rules:** 12 pt, 1.5 spacing, a cover
   page, and sections for research and issues, DAF/DoW impact, team and
   development plan, and technical approach with an explicit **hypothesis**. Up
   to 5 pages are allowed, so a figure fits.
3. **Fix the hardware claim.** The draft says powder will be made *"in-house
   by plasma-based ultrasonic atomization"*, but only the induction module is
   on hand. Suggested wording: in-house induction ultrasonic atomization now,
   with the plasma/arc module (the route Dodge et al. used for TiZrNbHfTa)
   requested through DURIP.
4. **Narrow the novelty sentence** (Section 2).
5. If Sayir signals no fit, also submit a methodology-first white paper to
   §A.2.c (Blasch). Each submission must say that more than one was submitted.
