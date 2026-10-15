# Mock Symposium-Organizer Review — Round 1

*For the TMS 2027 abstract [`tms-2027-lpbf-process-parameter-optimization-abstract.md`](../../tms-2027-lpbf-process-parameter-optimization-abstract.md).*
*Target symposium: **AI-Enabled Materials Processing: Integrating Accelerated Experimental Workflows and Processing-Aware Machine Learning**.*

> **Transparency / caveat.** Unlike the atomization-abstract review (which role-played named, verified
> organizers — Emma White, Hani Henein, an Ames Lab contact), the individual organizers of this AI symposium were
> **not verifiable** from public TMS 2027 pages at the time of writing. This review therefore role-plays a
> composite reviewer aligned with the symposium's **stated scope** (processing-aware ML + accelerated
> experimental workflows) and the broader AM-ML community, run as a mock pass rather than against named people.
> **Action:** confirm the organizer list on ProgramMaster and, ideally, re-run a named-organizer pass before
> submission.

---

## Reviewer persona

A processing-aware-ML / accelerated-experimentation reviewer: values closed-loop experimental workflows,
uncertainty-aware optimization, honest experimental-budget accounting, and physically grounded priors. Skeptical
of (a) "we used ML" with no methodological substance, (b) over-claimed autonomy, and (c) LLM window-dressing.

## Round-1 verdict

**Lean accept, conditional.** The workflow fits the symposium title almost exactly, and the cross-machine
transfer angle is genuinely interesting. But the draft as first written read as a **method laundry list** and
made two claims that would draw fire.

## Issues raised (and dispositions)

1. **"Sounds like a generic parameter-optimization study."** — For *this* symposium the AI/workflow contribution
   must lead, not the metallurgy. **Adopted:** opening now leads with the machine-specificity/transfer problem
   and the simulation-seeded, budget-aware loop; the escalating test ladder is framed as the *validation* of the
   optimization, not the headline.

2. **LLM layer risks reading as a gimmick.** A processing-aware-ML audience is wary of "we added an LLM." **Adopted:**
   scoped to a **pilot** that *augments* (drafts parameter sets, dispatches Thermo-Calc/optimizer tool calls,
   interprets SEM imagery) rather than an autonomous system — and grounded in real prior art (AdditiveLLM;
   Agentic AM Alloy Evaluation) in the scoping doc. Explicitly tests "where language-model reasoning usefully
   augments (rather than replaces) the statistical loop."

3. **Transfer claim could be over-read as solved.** **Adopted:** transferability is stated as an **open question we
   measure** ("we explicitly test how well an optimized window transfers … and how few experiments a
   transfer-aware model needs to re-qualify"), not a result. This is both more honest and more interesting to
   the room.

4. **"A couple dozen runs" — is that enough to matter?** For an early-stage group, a modest build count is fine
   **if** framed as budget-aware. **Adopted:** the abstract's takeaway explicitly includes "the experimental
   budget each requires," turning the small N into a feature (efficiency) rather than a weakness.

5. **Don't quote a density/parameter number you don't have yet.** **Adopted:** no specific D-value or window is
   asserted in the submission version; the Thermo-Calc Al6061 example (44.64–50 J/mm³ → ~99%) lives only in the
   scoping doc as motivating prior art, not as our result.

## Carried to round 2

- Whether to name a lead alloy (AlSi10Mg baseline + one lean Al) vs. staying powder-type-agnostic.
- Whether the LPBF-at-Utah partner (Taylor Sparks) is co-author or acknowledgement.
- Tightening the single long title.
