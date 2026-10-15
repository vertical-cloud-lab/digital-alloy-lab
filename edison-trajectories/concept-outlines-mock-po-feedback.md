# Mock Program-Manager Feedback on FLAIME Concept Outlines

*Edison Scientific ANALYSIS task `afc3b3c0-65ce-43ed-84b4-25cdc5acd96d`, submitted 2026-05-02 against the three single-page concept outlines in `concept-outlines/` (commit 4d44f30). Three in-character PM personas (NSF DMREF / DOE AMMTO+CMI / DARPA DSO) plus a cross-agency synthesis.*


### 1. NSF DMREF Persona (Dr. John Schlueter, DMR)

**(a) FIRST-IMPRESSION:** 
I skim the "Problem" section looking for the fundamental knowledge gap. I would probably stop reading closely halfway through the first paragraph. Framing the problem as "Replacing them requires jointly optimizing composition, atomization, and LPBF processing" is pure engineering. This reads like a process-optimization pitch, not fundamental materials science. Furthermore, saying "this concept formalizes that conversation" regarding a brief chat on a TIP panel is presumptuous—hallway chats are not green lights.

**(b) PROGRAM FIT:** 
Weak fit for DMR. DMREF is about discovering new materials paradigms and advancing the Materials Genome Initiative. Your goal is highly applied ("identify printable Al alloys that approach Al–Ce..."). You are treating the CALPHAD and BOFN loop as a tool to solve a supply chain problem, rather than using the loop to uncover new fundamental thermodynamics or physics of multi-principal element alloys. CMMI (Advanced Manufacturing) or the TIP Directorate are much better homes for this.

**(c) PARTNERSHIP STRUCTURE:** 
Proposing both Canada (NSERC) and Germany (DFG) tracks on a single DMREF is a massive administrative headache and structurally implausible for a $1.5M grant. You’d need both foreign agencies to independently approve and fund their PIs on the exact same timeline. Pick one. Also, NSF does not fund National Labs (Ames); they must bring their own funding.

**(d) PRELIMINARY-RESULTS CREDIBILITY:** 
You have a lot of hardware plugged in (atomizer, LPBF, HPC). A skeptical DMR reviewer will discount this entirely because it proves systems integration, not scientific capability. What would materially strengthen the case is preliminary evidence that your BOFN can actually navigate the complex thermodynamics of a 15-element space to find a fundamentally new phase, rather than just tweaking AlSi10Mg.

**(e) CONCRETE NEXT MOVE:** 
Polite redirect. I would reply: *"Sterling, it was good meeting you on the panel. While the closed-loop methodology aligns with MGI, the proposed scope is highly applied and focused on alloy optimization rather than fundamental materials discovery. I recommend looking into CMMI's Advanced Manufacturing programs or reshaping this to focus heavily on the underlying thermodynamics of the Al-systems."*

**(f) RED FLAGS (Current & Pending):** 
Stating that Genesis funds the "autonomous-platform integration" is a massive red flag. Reviewers will absolutely accuse you of double-dipping. To a panel, building the loop (DOE) and running the loop (NSF) look identical in a budget justification. You must explicitly partition the *science* (NSF) from the *hardware/software platform* (DOE).

***

### 2. DOE AMMTO / CMI Hub Persona

**(a) FIRST-IMPRESSION:** 
I read past the first paragraph because you hit the right buzzwords: domestic feedstocks, supply-risk objective, and TRL-4. The phasing of "reward annual, instrumented TRL deliverables" is a bit pandering (you clearly read our FOA), but it shows you understand our culture. You want to make a real thing that industry can use. I like that.

**(b) PROGRAM FIT:** 
Very strong fit for AMMTO Multi-Topic and the CMI Hub. Critical materials substitution (moving away from Co/Ni/REEs to Mn/Cr/Zr) is exactly our mandate. The alignment with the most recent DOE Critical Materials List is spot on.

**(c) PARTNERSHIP STRUCTURE:** 
BYU + CMI + Ames + Valimet is a solid stack. **Showstopper flag:** AMAZEMET is an EU-based hardware vendor. AMMTO is incredibly strict on Build America, Buy America (BABA) provisions and domestic supply chains. If you are pitching a domestic supply chain solution that relies on European atomization hardware, you need a bulletproof justification. Also, you omitted any mention of the mandatory 20% cost-share. Where is the money coming from?

**(d) PRELIMINARY-RESULTS CREDIBILITY:** 
The fact that you already have an Ames letter on file and are successfully running UA composition modification with standard Al wire strengthens your case immensely. A skeptical PM would question whether your algorithm can effectively ingest CMI's supply-risk metrics in a mathematically rigorous way, or if it's just a tacked-on penalty function.

**(e) CONCRETE NEXT MOVE:** 
Scoping call. I would reply: *"Sterling, the scope and cadence align well with CMI Hub objectives. Let's get a 30-minute call on the books with Ames. Please come prepared to discuss how you plan to meet the 20% cost-share requirement and your strategy for BABA compliance given the EU hardware."*

**(f) RED FLAGS (Current & Pending):** 
Claiming this is "narrower" and "independent" of Genesis Topic 3B isn't going to cut it. If Genesis is funding the loop, AMMTO is just funding the consumables and the specific CMI objective function. You need to frame Genesis as funding the *base platform construction* and AMMTO as funding a *specific, industrially relevant alloy development campaign*.

***

### 3. DARPA DSO Persona

**(a) FIRST-IMPRESSION:** 
I skim to see if this is "DARPA-hard" or just an engineering project. "Wire-/scrap-to-powder pathway producing LPBF-qualified powder" in theater is a highly compelling DoD capability. However, saying this is "off-program for FOA-driven offices" is arrogant—don't tell me how to view my portfolio. 

**(b) PROGRAM FIT:** 
Borderline. DSO takes fundamental science risks, not systems integration risks. You state: "the integration into a 12-month... demonstration is the risk DSO is positioned to take." **Wrong.** Integration is a risk for DLA or Army DEVCOM, not DSO. To fit DSO, the risk must be that the fundamental physics/metallurgy of deriving high-performance alloys strictly from battlefield scrap might be impossible, and your AI is the only way to crack the phase space.

**(c) PARTNERSHIP STRUCTURE:** 
JHU APL is a great transition partner. But if you are doing forward-deployed logistics and relying on CMI/Ames metrics, do you have the facilities and clearances to handle CUI/ITAR data? You don't mention security posture at all. 

**(d) PRELIMINARY-RESULTS CREDIBILITY:** 
The strongest result in all three notes is your SEM/EDS showing measurable composition shift from wire-to-powder. It proves the hardest physical step—in-situ alloying via UA—actually works. That buys you a lot of credibility.

**(e) CONCRETE NEXT MOVE:** 
I would reply: *"Send the 1-pager, but you need to heavily revise the 'Risk' section. DARPA doesn't fund systems integration. What is the fundamental technical barrier that makes this impossible today? Why hasn't anyone else done it? Focus on the metallurgical leaps, not just plugging an atomizer into an LPBF machine."*

**(f) RED FLAGS (Current & Pending):** 
*"The full proposal can reuse a substantial fraction of the Genesis Mission narrative."* **Never, ever say this to DARPA.** If a PM thinks you are sending them a recycled civilian DOE proposal, they will immediately delete your email. We fund unique, DoD-specific leaps, not civilian table-scraps. Pre-empt this by completely decoupling the DoD logistics narrative from the Genesis R&D narrative.

***

### SYNTHESIS 

**Strongest vs. Weakest:**
*   **Strongest:** The DOE AMMTO note. The cadence, metrics, and critical-materials focus perfectly align with the agency's mission.
*   **Weakest:** The NSF DMREF note. It completely misreads NSF's mandate, pitching an applied manufacturing optimization problem as a fundamental materials discovery effort.

**Is the PI overcommitting?**
Yes. You are a single PI at BYU with one primary piece of hardware (the AMAZEMET) and one algorithmic approach (pKGFN). Pitching this simultaneously as fundamental science (NSF), domestic supply-chain transition (DOE), and battlefield logistics (DARPA) while holding a pending DOE Genesis grant makes you look like a hammer frantically searching for three different nails. Reviewers talk; if you get caught pitching the same core loop everywhere, your credibility will take a hit.

**The Single Most Important Edit:**
Stop pitching the "FLAIME loop" as the core deliverable. The loop is just your tool. Pitch the *fundamental thermodynamics* to NSF, the *specific transitionable alloys* to DOE, and the *impossible logistics capability* to DARPA. 

**Other Agencies to Consider:**
*   **ONR (Naval Materials Division):** They are highly invested in expeditionary/shipboard AM and would love the wire/scrap-to-powder angle.
*   **NASA STMD (In-Space Manufacturing):** They have a massive mandate for recycling scrap material into usable print feedstock for long-duration missions. 
*   **DLA (Defense Logistics Agency) or Army DEVCOM:** Better fits for the systems-integration and logistics risk that DARPA DSO might reject.


---

## Round 2 — PDFs uploaded so Edison can interpret figures and layout

*Edison Scientific ANALYSIS task `115ffc21-7f98-4c1d-a5e6-c83f20cee259`, submitted 2026-05-02 against the same three concept-outline PDFs (commit 4d44f30). This time the PDFs were uploaded via `client.upload_file()` (returning `data_entry:UUID` handles) and passed as `files=[...]` to `client.create_task()` per the [Edison API docs](https://edisonscientific.gitbook.io/edison-cookbook/edison-client) — Round 1 only sent the prompt text and the PMs were therefore guessing at the layout. Notably, the PDFs were uploaded as `data_entry:5cb60365-…` (NSF), `data_entry:8e339786-…` (DOE), `data_entry:4d11d6cb-…` (DARPA).*

*The Round-2 panel actually inspected layout/typography/figures (Edison ran `pymupdf` to read the PDFs and even called out a line of text running off the right edge of the NSF outline). The most consequential deltas vs. Round 1 below.*

### Layout-aware critiques the Round-1 panel could not make
- **NSF DMREF (Schlueter):** *"...there is literally a line of text ('...composition/process/property/supply-risk') that runs completely off the right edge of the page. There are no figures. You need a diagram of your MGI loop, not a wall of 10pt Computer Modern text."*
- **DOE AMMTO:** *"The margins are actually readable on this one, though I still desperately want a flowchart of the pipeline rather than just text."*
- **DARPA DSO:** *"Visually, your right margin is 9 points wide—it's cramped, dense, and lacks a quad chart or a hero graphic. I can't take a wall of text to my Office Director to justify $3M."*

### New structural showstoppers Round 2 surfaced
- **AMMTO 20% statutory cost-share** is unmentioned in the DOE outline. *"If you don't explicitly mention your cost-share strategy in a DOE EERE pitch, I assume you haven't read the FOA rules."* Need to name who provides cost-share (Valimet/AMAZEMET in-kind hardware?).
- **NSF cannot fund Ames** as a partner — Ames must bring its own funding to a DMREF.
- **DARPA DSO mismatch confirmed and sharpened:** *"You're basically asking for money to turn the crank on a machine you already built."* Better fits per Edison: ONR (Naval Materials Division), Army DEVCOM, DLA.

### The single most important edit (Round 2)
> *Delete 25% of the text and insert a visual flowchart/DAG. None of these notes have figures. Federal PMs are visual skimmers. A single block diagram showing Input (Feedstock) → AI/CALPHAD Loop → Ultrasonic Atomization → LPBF → Testing would instantly communicate the scope, save hundreds of words, and fix the cramped, unreadable layout (especially the broken margins in the NSF document).*

### Cross-agency synthesis (Round 2)
- **Strongest:** DOE AMMTO (TRL framing + Ames/CMI alignment land cleanly with EERE culture, *if* cost-share is fixed).
- **Weakest:** DARPA DSO (misreads office culture; reads as a logistics/integration play to an office that funds TRL 1–2 fundamental physics breakthroughs).
- **Overcommit risk (PI-as-author hazard):** *"Federal PMs talk to each other. The PI risks looking like a tool-builder desperate to fund a specific machine, rather than a scientist solving an agency-specific mission."*
- **Other venues to consider:** ONR Naval Materials, Army DEVCOM (point-of-need manufacturing from scrap/wire), NIST MGI / CHIPS (closed-loop dataset + Bayesian algorithm angle).

### Concrete next moves before re-sending
1. Fix the NSF outline line-overflow bug (right-margin text getting cropped) — this is a literal layout defect the PM saw in <30 seconds.
2. Add a single DAG figure to all three outlines: Feedstock → CALPHAD/BOFN → UA → LPBF → Test → Loop closure.
3. NSF DMREF: drop one of the two international tracks; reframe around fundamental thermodynamics, not parameter optimization.
4. DOE AMMTO: add an explicit cost-share paragraph; remove Ames as a budgeted partner (keep as collaborator with own funding).
5. DARPA DSO: either redirect to ONR/DEVCOM/DLA, or reposition with a fundamental science thesis (e.g., a physics claim that is "impossible" under conventional UA/LPBF assumptions).
6. Across all three: tighten the Genesis-Mission scope-separation language — Round 2 still flagged it as the biggest current-and-pending risk.

### API-usage note (so this isn't repeated)
The Round-1 submission failed to attach the PDFs because bare filenames were passed as `files=[...]`. The correct pattern per the Edison cookbook is:

```python
fid = client.upload_file(file_path="concept-outlines/01_nsf_dmref.pdf")  # -> "data_entry:UUID"
client.create_task(task_data=TaskRequest(name=JobNames.ANALYSIS, query=...),
                   files=[fid, fid2, fid3])
```

Edison interprets PDF figures, tables, and layout when given `data_entry:` handles — Round 2 explicitly used `pymupdf` to render and inspect the PDFs, which is why the figure/margin/typography critiques only appeared this round.
