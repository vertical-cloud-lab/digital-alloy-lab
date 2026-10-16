# Mock organizer review — Round 2

**Symposium:** Novel Strategies for Rapid Acquisition and Processing of Large Datasets From Advanced
Characterization Techniques (TMS 2027)

> **Caveat:** role-plays the symposium *scope*, not named organizers (no live `EDISON_API_KEY` in the
> drafting runner). See `literature-scoping.md` for the named-organizer re-run.

## Draft reviewed
The round-1-revised, data-first submission version (144 words): opens with the characterization
bottleneck and two concrete failures, describes the closed-loop recommender across five modalities, names
the three grounding sources, and ends with orthogonal ICP-MS/MS validation + a shareable dataset.

## Panel feedback

1. **Scope claim resolved.** Leading with the acquisition/setup problem and the parameter-sweep dataset
   puts the abstract squarely in-scope. Good.

2. **Watch the ICP-MS/MS framing.** EDS/XRF are near-surface; ICP-MS/MS is bulk. Reviewers will want you
   to acknowledge you're benchmarking a near-surface technique against a bulk one, not claiming they
   measure the identical volume. **Recommendation:** keep "orthogonal" (already implies a different, not
   identical, measurement) and make the surface-vs-bulk distinction explicit in the talk. *Accepted as a
   talk-level note; the word "orthogonal" already signals this in the abstract.*

3. **Don't quote a single hero number you might revise.** The several-fold Mg overestimate and the
   ~40%→77% EBSD CI jump are safe because they're directional and already observed. Avoid committing to a
   final accuracy target (e.g., "±0.05 wt%") in the abstract itself — keep that as a goal in the scoping
   doc, not a promise on the ProgramMaster form. **Adopted** — the submission abstract says "emerging
   parameter–fidelity relationships," not a fixed accuracy figure.

4. **Credit the tacit-knowledge source without overloading the abstract.** The Standing/Paul beam-current
   insight is a nice story but belongs in acknowledgements/co-authorship, not the 150-word box. **Adopted**
   — flagged in the checklist and author-list note, kept out of the abstract body.

5. **"Supply-chain-resilient" is the right descriptor.** Consistent with the #98 resolution (avoids the
   "critical-mineral-lean" vs. Al–Ce contradiction). Keep it. **Adopted.**

## Verdict
**ACCEPT for an oral slot**, contingent on the standing author-list confirmation (add facility staff /
confirm presenter) and a live named-organizer review once the ProgramMaster organizer list is available.
No fatal flaws: the abstract is in-scope, quantitatively motivated, honestly scoped for an early-stage
group, and offers a dataset deliverable the symposium values.

## Remaining author-side to-dos (carried to the checklist)
- Confirm final author list + presenting author; consider Mike Standing / Paul.
- Verify symposium is accepting abstracts and confirm the deadline on ProgramMaster.
- Run the Edison `LITERATURE_HIGH` scoping prompt (`literature-scoping.md`) for a citation-backed
  deepening and a named-organizer review pass.
