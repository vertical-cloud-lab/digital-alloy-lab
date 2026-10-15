# Edison Review: Narrative Trim Plan

Task ID: 8fcb2f83-2703-4c58-98d1-68c332899f7b

Grade: B+

Short version: the plan is good and mostly sane, but 1.94 pages of savings is a little optimistic as written. I think you can get there, but only if you add one figure cut and treat S3 as the real compression target. The biggest miss in the current plan is that the narrative’s true space problem is not S6. It is S3.

Direct answers

1. Is ~1.94 pages savings realistic?
- Barely, and not from A1-A11 alone as currently estimated.
- My adjusted read is about 1.8-1.9 pages, with the main overestimates in:
  - A6 Project Management + Risk bullets: likely ~0.10 instead of 0.18 pages
  - A5 Genesis Mission compression: likely ~0.12 instead of 0.18 if done safely
  - A11 Objectives compression: likely ~0.05-0.08 instead of 0.10
- The big reliable cuts are A2, A3, A4, A1, A7, A8, A9.
- The hidden good news: S3 is larger than you think. From the PDF, S3 looks closer to ~3.1 pages, not 2.3. That means there is more compressible material there than your section budget assumes.

My conservative estimate:
- A1-A11 as described, executed safely: ~1.66-1.78 pages
- Add one figure cut: gets you comfortably above 1.9 pages

2. Any must-keep anchors threatened by A1-A11?
Yes, but only two need real protection.

- A4 CALPHAD compression is the highest-risk edit.
  Must keep in the narrative:
  - all 3 fidelity levels named
  - TCAl10 + TCMG6 + AM Module explicitly
  - async fairshare HPC framing
  - cost-aware pKGFN logic
  - reciprocal AM Module feedback loop from melt-pool cross-sections
  - SVDKL/deep-kernel GP for larger spaces
  Safe to move out:
  - MOBAL8
  - TC-PRISMA internals
  - L1₂-Al3Zr kinetics detail
  - solute-trapping detail
  - CET/G-R detail

- A5 Genesis Mission compression is riskier than your note suggests.
  I would not collapse this to 1 sentence. Keep 2 sentences minimum:
  - one sentence on AmSC hosting / GM participation / plug-and-play BOFN-pKGFN release
  - one sentence on FAIR deposition plus bidirectional use of GM data, with Appendix 4 forward reference

- A11: do not really merge O1 and O2 conceptually. Tighten wording, yes. But keep the distinction between:
  - O1 closed-loop autonomous platform
  - O2 breadth of compositional exploration

Everything else is low risk if done cleanly.

3. Higher-yield, lower-risk trim missed?
Yes. The safest missed cut is figure-based.

Top missed trim:
- Remove Fig 4 entirely.
  It is explicitly still a placeholder. In a 5-page limit narrative, a placeholder figure is expensive dead weight. That should be the first thing to go.
  Expected savings: ~0.20 pages.
  Reviewer risk: essentially zero.

Second missed trim:
- Trim Fig 1 to the CALPHAD panel only, or remove the placeholder EDS side.
  Right now Fig 1 also contains placeholder content. Keep the CALPHAD phase-landscape piece; that’s the useful credibility signal.
  Expected savings: ~0.08-0.12 pages.

On figure consolidation:
- Figs 1, 3, and 4 should not all stay as separate narrative figures under a 5-page cap.
- Best option:
  - keep Fig 2 in narrative
  - keep a trimmed Fig 1 in narrative
  - remove Fig 4
  - if still long, move Fig 3 to appendix
- I would not combine 3 and 4. Fig 3 is process architecture; Fig 4 is validation data. Different jobs.
- If tensile data arrives and you insist on keeping it, merge it into a trimmed Fig 1 or replace the placeholder panel in Fig 1.

4. Order of operations?
Build and measure after each major tranche. Don’t do all 11 blind.

Best sequence:
- Round 1: A1, A2, A3, remove Fig 4, then compile and measure
- Round 2: A4, A7, A9, trim Fig 1, then compile and measure
- Round 3: A6, A8, A10, A11, then compile and measure
- Round 4 only if needed: A5 plus fallback cuts

Reason: LaTeX page behavior is nonlinear. A “0.1 page” textual cut can become 0 pages until a float reflows, then suddenly become 0.3. You want measurement checkpoints after the big structural cuts, especially anything involving figures.

5. Safest fallback if you land at 5.2-5.3 pages?
Safest fallback: move Fig 3 to the appendix.

That is stronger and safer than compressing core technical content.
- Saves ~0.30-0.35 pages
- Low reviewer risk because the MVS progression is already described in text
- Natural appendix home: Facilities/Resources or Equipment

After that, safest micro-fallbacks are:
- compress LLAMBO to 2 sentences
- move MBS derivation/weighting rationale, but keep the definition inline
- remove the “Scaling behavior” sentence in S6
- compress the “Relationship to Prior Work” paragraph to 1 sentence and move it to S1

I would rank fallback safety:
1. Remove Fig 4
2. Move Fig 3 to appendix
3. Trim Fig 1 placeholder side
4. Compress LLAMBO
5. Move MBS derivation detail

6. Any content that should be repositioned for density?
Yes.

Best repositioning moves:
- Decision Gate Metrics: prose to table
  Columns: Metric | Definition | Phase I Target | Evaluation Method
  This likely saves space and improves scanability.

- Risk mitigation: prose to tight inline bullets or a 3-column mini-table
  Risk | Mitigation | Fallback

- Move “Relationship to Prior Work” from end of S3 into S1
  That paragraph is not methods. It belongs with credibility/context.

- Let Fig 2 do more work
  You currently both describe the BOFN DAG in prose and show it. Cut 2-3 prose sentences and let the figure/caption carry the structure.

I would not use sidebars or margin-note tricks. Too gimmicky for DOE and potentially format-risky.

7. Where would compression visibly hurt reviewer scoring?
Most sensitive sections by merit criterion:

- Relevance:
  visible risk if Genesis Mission integration gets too compressed. Keep this explicit.

- Technical Approach:
  visible risk if A4 hollows out the multi-fidelity logic too much. This is the section where compression can actually damage scoring.

- Team:
  low risk. PI pedigree can move to Appendix 5 if one strong sentence stays in the narrative.

- Milestones:
  low risk, since Table 1 is already efficient and should stay intact.

- Impact:
  moderate risk if Phase II gets compressed so much that Cu-Cr-Zr / 316H / Be-Cu pathway stops feeling credible. Keep the market, transfer path, and TRL ladder.

What I would not over-compress:
- the first-page differentiation block around supply disruption, LPBF exclusivity, and APEX/A-Lab/Peregrine gap
- the core multi-fidelity / async fairshare / cost-aware BOFN logic
- the quantitative gate metrics

What I would compress aggressively:
- placeholder figures
- PI pedigree detail beyond one sentence
- solver internals
- Phase II robotics implementation detail
- repetitive Genesis/FAIR language
- redundant mineral-burden explanation

Bottom line
- Your plan is good, but it needs one extra low-risk structural cut.
- The cleanest upgrade is: add “remove Fig 4 entirely” now.
- If still long, the next safest move is “move Fig 3 to appendix.”
- Don’t compress Genesis Mission to one sentence.
- Don’t let A4 strip out the named fidelity stack and async cost-aware logic.

Top 3 improvements
- Remove Fig 4 entirely; it is placeholder-only and buys ~0.20 pages at near-zero risk.
- Reframe S3 as the true target; do A2 + A4 first and measure before polishing smaller sections.
- Make Fig 3 the planned fallback to appendix rather than squeezing more core method prose.

[Discretionary analytical decisions made during the analysis]
- Estimated section page footprints directly from PDF page occupancy rather than accepting the provided section estimates at face value.
- Treated S3 as approximately 3.1 pages based on observed span from pages 4-7, because figure and text placement suggested the user’s 2.3-page estimate was low.
- Evaluated trimming-yield realism conservatively by discounting estimates for formatting-dependent edits such as bullet conversion and objective reformatting.
- Classified reviewer-risk primarily against DOE-style merit criteria: Relevance, Technical Approach, Team, Milestones, and Impact.
- Prioritized figure removal/repositioning over compression of core technical prose when identifying safest fallback cuts.
- Recommended iterative compile-and-measure checkpoints after major edit tranches rather than a single end-stage measurement, because float reflow can change effective page savings nonlinearly.
- Treated Genesis Mission integration as requiring at least two explicit narrative sentences despite the proposed one-sentence compression, based on FOA salience and reviewer visibility.
- Considered placeholder figures as lower-value narrative content than text-based technical anchors, and therefore higher-priority trim targets.