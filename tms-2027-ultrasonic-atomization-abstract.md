# TMS 2027 Abstract — Ultrasonic Atomization Parameter Tuning and Modeling

**Working title:** Optimizing Ultrasonic Atomization Parameters for Supply-Chain-Resilient Aluminum Powders in Laser Powder Bed Fusion

**Authors (all Brigham Young University):**

| Author | Email | Role |
| --- | --- | --- |
| Gage Erickson | [student email removed] | Presenting author |
| Ronnie Guymon | [student email removed] | Co-author |
| Xavier Zaitzeff | [student email removed] | Co-author |
| Carl Robison | [student email removed] | Co-author |
| Sterling Baird | sterling.baird@byu.edu | Corresponding author / PI |

**Meeting:** TMS 2027 Annual Meeting & Exhibition, March 14–18, 2027, Orlando, FL
**Presentation preference:** Oral Presentation
**Symposium:** Atomization & Powder Metallurgy for Advanced Applications: An MPMD Symposium Honoring Iver Anderson
**Abstract submission:** Now open via [ProgramMaster](https://www.programmaster.org/TMS2027) ([TMS2027 technical program](https://www.tms.org/TMS2027/TMS2027/Programming/TMS2027_Technical_Program.aspx))

> Context: part of the FLAIME project on AI-guided, critical-mineral-lean aluminum alloy discovery for additive manufacturing. Companion to the closed-loop AI optimization and powder-production work tracked elsewhere in this repo (see [Publication Strategy](edison-trajectories/publication_strategy.md)).

---

## Abstract (submission version, 145 words)

Iver Anderson's career defined oxygen control and fine-powder yield as major challenges for aluminum
additive-manufacturing feedstock. Ultrasonic atomization can act as a rapid alloy-screening route to
laser powder bed fusion (LPBF) feedstock, but this has been largely unstudied for novel,
supply-chain-resilient aluminum alloys in the US. We assemble a parameter-property dataset from dozens
of in-house ultrasonic atomization runs on an AMAZEMET rePOWDER system, deliberately spanning
domestically secure and import-reliant compositions from a palette of 15 non-aluminum alloying elements
(Mn, Cr, Zr, Mg, Si, Cu, Ti, Fe, Ni, Ce, Sc, Li, Er, Zn, Sn). We vary vibration amplitude, melt
superheat, and atomization atmosphere, and characterize particle size distribution (including the
sub-45 μm fraction), sphericity, satellite content, flowability, and oxygen pickup. For selected
compositions we perform LPBF single-track scans with cross-sectional melt-pool characterization. We
leverage statistical models to guide experimental design and identify compositions meriting
gas-atomization scale-up.

---

## Expanded / alternate version (leans harder into the multi-alloy, multi-run dataset)

Iver Anderson's career defined oxygen control and fine-powder yield as the gating quality challenges
for aluminum additive-manufacturing feedstock. Building on that legacy, this work asks whether
ultrasonic atomization (UA) — a capillary-wave breakup process distinct from gas atomization — can act
as a rapid alloy-screening route to laser powder bed fusion (LPBF) feedstock, a question largely
unstudied for novel, supply-chain-resilient aluminum. We assemble a
parameter–property dataset from dozens of UA runs on an AMAZEMET rePOWDER system, deliberately spanning
compositions designed from a palette of roughly 15 non-aluminum alloying elements that mix import-reliant
and domestically abundant sources: a standard commercialized composition (AlSi10Mg) that anchors the
dataset to known behavior, and lean experimental compositions (e.g., Al–Mg–Si, Al–Ce — the latter
leveraging cerium, an abundant co-product rare earth) that probe the edges of the
process window. Across this matrix we systematically vary vibration amplitude, melt superheat, and
atomization atmosphere, and characterize particle size distribution, the sub-45 μm fraction relevant to LPBF,
sphericity, satellite content, flowability, and oxygen pickup. Because UA of aluminum is known to risk
elevated oxygen and coarse median sizes, we treat both as quantities to be measured and bounded rather
than assumed. The breadth of the dataset lets us ask how composition shifts the usable process window and
where UA feasibly produces LPBF-relevant powder. Statistical and machine-learning models relate
atomization parameters to powder quality, informing a data-driven optimization of the atomization-to-print
workflow; we present composition-specific processing windows and discuss how UA screening can guide alloy
selection for subsequent gas-atomization scale-up of the most promising supply-chain-resilient aluminum
compositions.

---

## Referenced version (with in-text citations)

> **Note:** This version carries in-text citations for the Iver Anderson claim and the other
> load-bearing factual statements (UA particle-size behavior, oxygen pickup, the cerium /
> supply-chain-resilient rationale). It is **not** for the ≤150-word ProgramMaster box — the
> citation markers push it over the limit. Use it where references are allowed (e.g., a proceedings
> manuscript, an extended/poster abstract, internal review, or a grant/report blurb). All references
> are real, peer-reviewed sources surfaced during the Edison organizer review (DOIs below). Submit
> the [144-word version](#abstract-submission-version-144-words) to ProgramMaster.

Iver Anderson's work established oxygen control and fine-powder yield as defining challenges for
aluminum additive-manufacturing feedstock [1,2]. Building on that legacy, this study asks whether
ultrasonic atomization (UA) — a capillary-wave breakup process distinct from the aerodynamic
breakup of gas atomization [3,4] — can serve as a rapid alloy-screening route to laser powder bed
fusion (LPBF) feedstock for supply-chain-resilient aluminum compositions. We conduct dozens of UA
campaigns on an AMAZEMET rePOWDER system [5] across aluminum alloys drawn from a palette of roughly
15 non-aluminum elements spanning import-reliant and domestically abundant sources — from commercial
AlSi10Mg to lean experimental compositions, including Al–Ce, where cerium is leveraged as an
abundant co-product rare earth whose use stabilizes rather than strains the supply chain [6,7].
We vary vibration amplitude, melt superheat, and atmosphere, characterizing particle size
distribution, the sub-45 μm fraction relevant to LPBF — a demanding cut for UA aluminum, whose
medians often sit above 45 μm [5,8] — sphericity, satellite content, flowability, and oxygen pickup,
treating oxygen as a known UA limitation to be quantified rather than assumed [8]. Statistical and
machine-learning models relate atomization parameters to powder quality, yielding composition-specific
processing windows and guiding alloy selection for subsequent gas-atomization scale-up [1].

**References**

1. I. E. Anderson, E. M. H. White, R. Dehoff. "Feedstock powder processing research needs for additive
   manufacturing development." *Current Opinion in Solid State & Materials Science* **22**(1), 8–15 (2018).
   doi:[10.1016/j.cossms.2018.01.002](https://doi.org/10.1016/j.cossms.2018.01.002)
2. I. E. Anderson, J. C. Foley. "Determining the role of surfaces and interfaces in the powder
   metallurgy processing of aluminum alloy powders." *Surface and Interface Analysis* **31**(7),
   599–608 (2001). doi:[10.1002/sia.1087](https://doi.org/10.1002/sia.1087)
3. M. Zach et al. "Spherical powders: control over the size and morphology of powders for additive
   manufacturing and enriched stable isotope nuclear targets." *EPJ Web of Conferences* **285**, 03002
   (2023). doi:[10.1051/epjconf/202328503002](https://doi.org/10.1051/epjconf/202328503002)
4. I. E. Anderson, R. L. Terpstra. "Progress toward gas atomization processing with increased
   uniformity and control." *Materials Science and Engineering: A* **326**(1), 101–109 (2002).
   doi:[10.1016/S0921-5093(01)01427-7](https://doi.org/10.1016/s0921-5093(01)01427-7)
5. K. D. Ukabhai, D. Mkhonto, M. Phasha. "Investigation of Al–Cu using different preparation methods
   on the AMAZEMET rePOWDER machine." *MATEC Web of Conferences* **417**, 03001 (2025).
   doi:[10.1051/matecconf/202541703001](https://doi.org/10.1051/matecconf/202541703001)
6. Z. C. Sims et al. "How cerium and lanthanum as coproducts promote stable rare earth production and
   new alloys." *Journal of Sustainable Metallurgy* **8**, 1225–1234 (2022).
   doi:[10.1007/s40831-022-00562-4](https://doi.org/10.1007/s40831-022-00562-4)
7. R. T. Nguyen et al. "Anticipating impacts of introducing aluminum–cerium alloys into the United
   States automotive market." *Resources, Conservation and Recycling* **144**, 340–349 (2019).
   doi:[10.1016/j.resconrec.2019.02.009](https://doi.org/10.1016/j.resconrec.2019.02.009)
8. A. Yankin, H. A. Murtaza, B. Golman, A. Perveen, D. Talamona. "Effect of ultrasonic atomization
   parameters on AlSi12 aluminum powder characteristics for additive manufacturing." *Scientific
   Reports* **15**, (2025). doi:[10.1038/s41598-025-06086-7](https://doi.org/10.1038/s41598-025-06086-7)

---

## Symposium selection (TMS 2027)

**✅ Selected — submitting here (Oral Presentation):**

1. **Atomization & Powder Metallurgy for Advanced Applications: An MPMD Symposium Honoring Iver Anderson.**
   This is the strongest fit by a wide margin. It is the dedicated atomization/powder-metallurgy
   symposium, and it honors Iver Anderson (Ames Lab), a foundational figure in metal powder
   atomization. The abstract's core contribution — a systematic ultrasonic-atomization
   parameter study producing LPBF-grade aluminum powder — is squarely on topic, and the
   audience is exactly the powder-production community we want feedback from. (Ames is also a
   FLAIME letter-of-support partner, so the room is strategically valuable.)

**Strong alternatives (pick based on how the talk is framed):**

2. **Additive Manufacturing and Innovative Feedstock Processing for Multifunctional Materials.**
   Best fit if we frame the talk around feedstock-for-AM and the atomization→printability link
   rather than atomization fundamentals. Emphasizes the "novel feedstock processing" angle.

3. **AI-Enabled Materials Processing: Integrating Accelerated Experimental Workflows and
   Processing-Aware Machine Learning.**
   Best fit if we lead with the closed-loop AI optimization and the predictive
   parameter–property modeling across the multi-alloy dataset, treating atomization as the
   process being learned. Aligns with FLAIME's autonomous-experimentation narrative.

**Decision:** Symposium 1 (Honoring Iver Anderson) is the confirmed submission target, presented
as an **Oral Presentation**. The abstract as written is atomization-experiment-forward
(parameters → powder properties), which fits this symposium directly. Symposiums 2 and 3 remain
documented above as fallbacks only if Symposium 1 is oversubscribed; submitting the same abstract
to more than one symposium is discouraged by TMS.

---

## Pre-submission checklist (per TMS abstract guidelines)

- [x] Confirm final author list and presenting author; verify affiliations/emails. — 5 authors
      confirmed (all BYU), Gage Erickson presenting, Sterling Baird corresponding/PI; emails listed above.
- [x] Choose oral vs. poster preference. — **Oral Presentation.**
- [x] Select target symposium. — **Atomization & Powder Metallurgy for Advanced Applications:
      An MPMD Symposium Honoring Iver Anderson.**
- [x] Trim to the symposium's word limit (TMS abstracts are typically ~150 words / 1500 characters). —
      submission version is **145 words** (≤150, per `wc -w`).
- [x] Acknowledge the honoree's legacy and position UA as a screening complement to gas atomization
      (not a competitor or a direct-transfer claim). — opening line now ties to Anderson's oxygen/yield
      work; "transfer to commercial gas atomization" softened (round 3) to "guide alloy selection for
      subsequent gas-atomization scale-up."
- [x] Resolve the "critical-mineral-lean" vs. Al–Ce contradiction. — cerium is a USGS-listed critical
      mineral (an abundant, low-value co-product rare earth), so describing an Al–Ce alloy as
      "critical-mineral-lean" is contradictory; submission version now says **supply-chain-resilient**.
- [x] State a concrete, results-oriented takeaway. — **Round-3 organizer review advises against**
      locking in a specific D50 or oxygen ppmw at this stage: for an early-stage group the downside of a
      preliminary number that later shifts outweighs the credibility gain (UA-Al literature shows wide
      scatter, e.g., D50 ≈ 65 μm for Al–10Cu on rePOWDER, up to 37.5% PSD-span variation for AlSi12).
      "Dozens of UA campaigns" is kept unless a final, non-changing count is available before the deadline.
      Decision: keep the hedged "emerging parameter–property trends … will be reported" phrasing.
- [x] FLAIME is no longer named in the abstract body (removed per author request), so no acronym
      spell-out is needed; AMAZEMET / rePOWDER is retained as the named system (good specificity
      reviewers like).
- [ ] Note FLAIME / DOE funding acknowledgement if required by the program.
- [ ] Verify the symposium is accepting abstracts and check the submission deadline on ProgramMaster.

## Mock symposium-organizer review (Edison Scientific)

Four rounds of mock review were run through Edison Scientific, role-playing the actual symposium
organizers (Emma M. White, DECHEMA; Hani Henein, U. Alberta; an Ames National Laboratory organizer),
with the explicit caveat that this is an early-stage group with a limited atomization track record. Full
transcripts and the literature citations behind each point are in
[`edison-trajectories/tms-2027-abstract-review/`](edison-trajectories/tms-2027-abstract-review/)
([round 1](edison-trajectories/tms-2027-abstract-review/round1-organizer-feedback.md),
[round 2](edison-trajectories/tms-2027-abstract-review/round2-organizer-feedback.md),
[round 3](edison-trajectories/tms-2027-abstract-review/round3-organizer-feedback.md),
[round 4](edison-trajectories/tms-2027-abstract-review/round4-organizer-feedback.md)).

Round 1 changes adopted: open with Anderson's oxygen/yield legacy; reframe UA as a rapid alloy-screening
route rather than a gas-atomization competitor; remove the "transfer to commercial gas atomization"
claim; reframe the 15–45 μm window as a *recoverable fraction to be measured*; treat oxygen pickup as a
known UA limitation to be quantified; and replace "closed-loop AI optimization / predictive models" with
the more defensible "data-driven optimization" and "parameter–property trends."

Round 2 verdict: "would likely be accepted for an oral presentation" once the one remaining issue was
fixed — the contradiction of labeling an Al–Ce alloy "critical-mineral-lean" when cerium is itself a
USGS-listed critical mineral (abundant co-product rare earth). Adopted: switch the descriptor to
**supply-chain-resilient**, tighten the alloy enumeration (AlSi10Mg, lean Al–Mg–Si, Al–Ce), and note the
cerium co-product rationale in the expanded version.

Round 3 verdict: **"ACCEPT for an oral slot"** — the supply-chain-resilient framing is now internally
consistent and free of the prior contradiction, the Anderson opening and honest oxygen framing are
accurate, and "no fatal flaws remain." Two minor wording refinements were recommended and adopted:
(i) "the recoverable 15–45 μm fraction" → **"the sub-45 μm fraction relevant to LPBF"** (avoids implying a
high yield in the LPBF cut, since UA-Al medians often sit above 45 μm); and (ii) "inform subsequent
gas-atomization trials" → **"guide alloy selection for subsequent gas-atomization scale-up"** (UA realistically
de-risks alloy choice, not specific GA process parameters). The committee also advised *against* quoting a
specific D50/oxygen number at this early stage (see checklist). Submission version remains 132 words.

Round 4 verdict (on the PI-revised 15-element / LPBF-single-track candidate): **"ACCEPT for oral slot,
contingent on two minor wording fixes"** — both adopted. The panel confirmed the explicit 15-element
palette *strengthens* credibility over the earlier three-alloy enumeration and that the "domestically
secure and import-reliant" phrasing is honestly bifurcated (it does not claim Sc/Ce/Er are secure).
Adopted: (i) "(sub-45 μm powder **yield**)" → **"(including the sub-45 μm fraction)"** (the yield-implying
wording reintroduced the round-3 over-claim risk, since UA-Al medians often sit above 45 μm); and
(ii) the blanket "perform LPBF single-track melt pools …" → **"For selected compositions we perform LPBF
single-track scans with cross-sectional melt-pool characterization"** (scopes the printing work as
targeted, not exhaustive, for an early-stage group). The trailing double-"inform" was also tightened to
"identify compositions meriting gas-atomization scale-up." Submission version is now 145 words (≤150).

## Reference / model abstract

- Example of comparable published work (provided in the issue): Nature *Scientific Reports*,
  [s41598-025-06086-7](https://www.nature.com/articles/s41598-025-06086-7).
