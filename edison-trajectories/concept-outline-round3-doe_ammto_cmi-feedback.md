# Round-3 Edison feedback — doe_ammto_cmi

Task: `3693bf31-7609-44fc-ad8b-c58f995ac98b`

---

(a) FIRST-IMPRESSION
Keep reading. The page looks like someone actually thought about how AMMTO reads these things: a specific program line is named up top, the opening metadata line gives duration and budget range, and the little process schematic tells me in five seconds this is discovery-to-powder-to-LPBF-to-test, not another vague “AI for materials” note. What helps most is the opening problem statement getting to the agency point fast: “substitution toward domestically abundant Mn/Cr/Zr/Si/Fe streams” and the explicit comparison to the Al-Ce to Eck to Magna path. What still hurts in the first 30 seconds is the density. The body is one big wall of full-width text at about 10 pt with very long line lengths, so I’m interested, but I’m also bracing for work.

(b) PROGRAM FIT
This is directionally in family with an AMMTO Multi-Topic / CMI-linked concept, but it is not yet fully locked to a real program element.

What fits:
- The core problem is manufacturing-linked critical-materials substitution in a domestic feedstock context, not basic alloy science for its own sake.
- The deliverable framing is closer to AMMTO than to a pure BES-style concept: “UA powder spec, LPBF parameter window, and tensile data at room and elevated temperature” is the right kind of applied package.
- The CMI angle is credible where you say the loop “explicitly carries a feedstock supply-risk objective alongside printability and elevated-temperature strength.” That is the part that makes this more than an AM process optimization project.
- Referencing the Al-Ce commercialization trajectory is smart because it points to a DOE-recognizable handoff model.

What does not yet fit cleanly:
- The concept still reads as a platform-enabled discovery campaign first, and an AMMTO deployment-facing manufacturing project second. “pKGFN BOFN over CALPHAD multi-fidelity nodes” is fine for the technical team, but for AMMTO I need the project center of gravity to be manufacturing outcomes and industry pull, not the model stack.
- You have not pinned the proposed alloy family tightly enough to the most recent DOE Critical Materials List. Saying current printable Al systems rely on “Co/Ni/Sc/REE additions” is not the same thing as proving the target substitution materially changes exposure to listed critical materials in a way DOE would care about now.
- “One alloy family per project year” is a useful internal cadence, but it is ambitious relative to a TRL-4 expectation if each family requires powder production, LPBF windowing, reproducibility, and elevated-temperature data.
- If the intended endpoint is truly TRL-4, I’d want a clearer statement of the validation environment. Right now it is halfway between discovery-loop validation and manufacturing-relevant validation.

Bottom line: plausible fit for an AMMTO/CMI partnership conversation, but only if the white paper shifts the center of mass from algorithm novelty to domestic supply-risk reduction plus a specific manufacturing deliverable for a specific alloy class.

(c) PARTNERSHIP STRUCTURE
There are no immediate fatal flaws, but there are several places I’d push hard before encouraging a full submission.

- Cost share: You say the 20% non-federal share will be met by in-kind contributions from Valimet and AMAZEMET plus BYU summer salary/HPC. That can work in principle, but it will get audited on allowability, valuation, and period-of-performance alignment. “Characterization time,” “hardware access,” and “engineering support” are the kinds of items that need to be documented very cleanly or they become soft cost-share.
- CMI/Ames structure: The sentence “Ames brings its own DOE funding rather than receiving a budget line through BYU” is the right instinct. Keep that. It avoids a bad structure where federal funds are accidentally treated as match. But if Ames is doing “cross-check production runs” and “reference validation prints,” you need to spell out whether that work is entirely outside the proposed project budget and how data/IP handoff is managed.
- BABA: This is the shakiest compliance section. You are trying to solve it by saying the BYU-owned AMAZEMET unit is installed in the U.S. and that AMAZEMET’s role is “upstream engineering support, not procurement of foreign-manufactured end product.” That is not yet enough. BABA analysis turns on what counts as the manufactured product, what federal funds touch, and whether the project is assistance for infrastructure versus R&D equipment and produced articles. If the argument is that the deliverable hardware chain remains domestic because the relevant article is the powder-to-coupon-to-tested article stream, say that much more cleanly and be ready for counsel/contracting to disagree.
- Foreign entity exposure: AMAZEMET plus “EU mirror-site engineering support” is exactly the kind of phrase that will trigger a second look. Not an automatic disqualifier, but it raises supply-chain and data-sharing questions.
- Security posture: Nothing here addresses research security, controlled data, cyber hygiene, or export-control screening for foreign partner interaction. For an unsolicited one-pager that’s not disqualifying, but for this topic area it is an omission.
- Industrial pull: Valimet is helpful. Thermo-Calc is not really an industrial transition partner; it is a tools vendor. The concept still lacks the downstream user analogous to Eck/Magna. Right now I see comparator powder, hardware, software, and a national lab. I do not yet see the company that would care enough to qualify and carry the alloy into a real manufacturing setting.

(d) PRELIMINARY-RESULTS CREDIBILITY
Mixed. The preliminary work proves that the team is building the machinery, but not yet that the proposed AMMTO risk is being retired.

What is credible:
- “UA composition modification from AlSi10Mg + Al wire + Si feed confirmed by SEM/EDS” shows you can actually perturb feedstock using the atomization route you want to sell.
- “working pKGFN BOFN implementation” and “CALPHAD jobs on BYU HPC” show the computational loop is not imaginary.
- “AlSi10Mg LPBF tensile baseline” is the right kind of anchor dataset.

What is missing for this agency:
- None of the listed preliminary results shows a candidate domestic-feedstock substitution alloy printed and tested with even an early property/process window.
- “Elevated-temperature tensile data on a standard Al specimen” is weak evidence for this application. It proves a test capability, not a project-specific technical inflection.
- The Ames support letter helps administratively, but it is not technical de-risking.

The single additional preliminary result that would help most: one actual LPBF coupon set from a target Al-Mn-Cr-Zr or Al-Zr composition produced via the proposed feedstock route, with basic printability evidence plus at least room-temperature tensile results benchmarked against AlSi10Mg and a short statement of supply-risk advantage relative to an Sc- or REE-bearing comparator. One real closed-loop example beats five pieces of platform plumbing.

(e) FIGURES / LAYOUT / TYPOGRAPHY
The top pipeline figure is useful. It is not really a DAG in the formal sense, but it functions as a compact workflow: Feedstock -> CALPHAD -> pKGFN BOFN -> Ultrasonic Atomization -> LPBF -> Test, with a dashed loop-closure arrow back from test to the BOFN region. That works.

Concrete visual notes:
- The figure is vector-clean and does not run off the page. No text is visibly clipped.
- The box colors are restrained and readable; the step labels are understandable.
- The weak point is font size inside the boxes. The sublabels are very small, around the 5.6–6.4 pt range in the rendered PDF. On screen I can read them if I zoom. Printed or forwarded as an email attachment, that will be annoying.
- Body text is dense, full-width, and long-measure. The usable text width is roughly 7.4 inches on letter paper, with about 0.5-inch side margins. That makes for very long lines and a “grant wall” feel.
- The bold section headers help a lot. “Problem,” “Idea, deliverable cadence, and go/no-go,” “Cost-share and BABA compliance,” etc. are the right headings for this audience.
- The opening metadata line is good, but it is crowded. I’d keep PI / solicitation / type / keywords, but simplify the punctuation and reduce the number of bold interruptions.
- No obvious text runs off the edge. Margins are tight but intact. Bottom spacing is fine.
- The GitHub link at the bottom is visually louder than it needs to be. For this audience, repository is secondary to transition path.

(f) CONCRETE NEXT MOVE
Sterling — thanks for sending this. I see a plausible AMMTO/CMI conversation here, especially the domestic-feedstock substitution angle and the attempt to define an annual TRL-4 package, but before I’d encourage a white paper I’d want you to tighten three things: exact linkage to the current DOE Critical Materials List, a cleaner BABA/cost-share treatment, and one real preliminary closed-loop LPBF result on a target substitution composition. If you can sharpen those points, I’d be open to a short scoping call with the relevant AMMTO lead and Ames/CMI contact.

(g) RED FLAGS — CURRENT & PENDING / DOUBLE-DIPPING
I would still flag this for future panel attention.

The separation language is better than the usual hand-wave. You do say: “Genesis Mission funds platform construction ... this AMMTO scope funds a specific industrially relevant alloy-development campaign” and “no budget line is shared.” That is the right structure.

But I am not fully convinced yet because the technical heart of this concept is still the FLAIME discovery loop itself. If the same personnel, same software stack, same data fabric, same scheduler, and same autonomous experimentation backbone are doing the real work in both efforts, then “platform” versus “campaign” can collapse pretty fast in panel discussion. The more the concept emphasizes pKGFN/BOFN/CALPHAD infrastructure, the easier it is for a reviewer to say the AMMTO project is just an application layer riding on Genesis-funded core capability.

What would make me more comfortable is explicit scope-separation language at the task level: Genesis builds and maintains the general platform; AMMTO funds only campaign-specific alloy design, powder production, LPBF parameterization, validation testing, and supply-risk benchmarking for named alloy families, with separate labor accounting and separately itemized data packages. Without that specificity, I’d keep a yellow flag on double-dipping.

(h) DELTA VS ROUND 2
I cannot verify the prior Edison critique because task 115ffc21 is not retrievable from the available workspace or platform state. So I cannot do a true side-by-side against the earlier draft. What I can say is what this revised version now does well, what remains weak, and what the revision appears to have introduced as new exposure.

Materially better in this draft:
- It now speaks in program language instead of generic research language. The phrases “20% statutory non-federal cost-share,” “BABA,” “TRL-4,” and “current-and-pending” tell me the PI heard at least some commercialization/compliance feedback.
- The annual go/no-go is much clearer than a generic success claim. Listing “UA powder spec, LPBF parameter window, and tensile data” is a real deliverable frame.
- The Ames/CMI role is more cleanly described as a collaborator with its own funding rather than a subaward-shaped blur.
- The Al-Ce -> Eck -> Magna analogy is now used appropriately as a transition precedent rather than as decoration.
- The request at the end is sensible: a scoping call before writing a full white paper.

Still weak:
- Critical-materials alignment is asserted, not demonstrated. You still need a crisp mapping from target substitution chemistry to the current DOE list and to a manufacturing-relevant domestic-supply problem.
- Preliminary data are still platform-heavy and campaign-light.
- The partner stack still lacks a true downstream adopter who would make the transition story feel real.
- BABA remains lawyer-bait. The current text is thoughtful, but not yet persuasive.
- The cadence may still be overpromised relative to the amount of experimental validation implied by “one alloy family/year.”

New issues this revision introduced:
- By adding explicit BABA language, you have now put a compliance question on the table that reviewers may not have focused on otherwise. Because AMAZEMET is named alongside “EU mirror-site engineering support,” that section now invites scrutiny.
- By naming the pending Genesis Mission Topic 3B proposal directly, you improved transparency, but you also sharpened the double-dipping question. You now need stronger task-level separation than the concept currently provides.
- The concept is more PM-aware now, but also denser. The added compliance and scope-separation text pushes the page closer to the limit of what is digestible in one pass.

- Discretionary analytical decisions made during the analysis
- Used the rendered PDF plus extracted text spans to assess typography and layout rather than relying on text extraction alone.
- Treated this as an unsolicited concept-note critique in program-manager voice, not a formal FOA merit review.
- Assessed BABA as a compliance risk area rather than making a definitive legal determination, because the document is a concept outline and not a full assistance application.
- Framed section (h) with an explicit limitation because the prior Edison task 115ffc21 was not retrievable from the available workspace/platform state.
- Interpreted the top schematic as a workflow/loop-closure figure rather than requiring strict graph-theoretic DAG semantics.
- Used approximate PDF span sizes and page geometry to comment concretely on readability, margins, and figure legibility.
