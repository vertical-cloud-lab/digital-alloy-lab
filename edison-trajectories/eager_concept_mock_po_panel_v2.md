# Edison Scientific: Mock NSF PO Memos v2 (3 distinct POs) on REVISED EAGER Concept Outline

*Edison Scientific ANALYSIS query — Job: `job-futurehouse-data-analysis-crow-high`*
*Task ID:* `33484db0-ab7f-4684-a050-07f2e808c523` (submitted 2026-05-02)
*Uploaded file:* `eager-concept-outline.pdf` (revised) → `data_entry:24b33567-2172-48b2-9486-a27ea7758fd0`
*Submission script:* `/tmp/edison_eager_mock_po_v2.py`

**Context:** Second mock-PO panel after revising the concept outline to address the v1 panel's three convergent concerns (MX-100 fitness + measurement protocols, BOFN problem statement + data flow, powder QC + DMR-vs-CMMI framing) and adding a compact risk-mitigation row. POs were chosen by the model rather than user-specified.

**Concept reviewed:** [`eager-concept-outline.pdf`](../eager-concept-outline.pdf) (revised; compiled from [`eager-concept-outline.tex`](../eager-concept-outline.tex)).

---

# Internal NSF EAGER Review Simulation: FLAIME-VCL

**Selected Program Officers (ENG/CMMI Advanced Manufacturing)**
1. **Linkan Bian**: Currently serving as a CMMI AM program director (rotator from Mississippi State University). His core research expertise is precisely in machine learning for additive manufacturing, digital twins, and Bayesian optimization in AM.
2. **Khershed Cooper**: Long-serving CMMI AM program director with a deep background in materials science (NRL) and nanomanufacturing/advanced manufacturing platforms. He often evaluates multi-station hardware integrations and material scaling.
3. **Andrew B. Wells**: Currently serving CMMI AM program director with a focus on "hard tech" implementation, manufacturing workforce expansion, and scalable hardware architectures. 

*Note: While the previous panel featured Kevin Chou and Alexis Lewis, current NSF directory data for the CMMI AM cluster highlights Bian, Cooper, and Wells as the active managing POs for this domain.*

---

## Linkan Bian (Rotator, AM Data & Machine Learning)

**Why this would land on my desk:**
My core expertise at Mississippi State was data-driven modeling and Bayesian optimization for additive manufacturing. This proposal directly employs a Bayesian Optimization over continuous parameter spaces (BOFN) to drive LPBF processing conditions without human intervention, which sits dead-center in my portfolio.

**What I like (after the revisions):**
The PI clearly listened to the previous feedback. Tightening the BOFN problem statement to something concrete (maximizing Vickers hardness constrained by ≥99% Archimedes density) with defined design variables (laser power, scan speed, hatch spacing, layer thickness) gives me confidence they actually know how to deploy the math. The 20-cycle budget is realistic for a physical AM campaign. I also appreciate the explicit data-flow sketch connecting the OM/hardness features to HDF5/JSON metadata before feeding the BOFN. The laser tracker and 1 kHz MEMS accelerometer metrology for the go/no-go gates is a rigorous way to validate the hardware.

**What still worries me:**
The PI explicitly scoped *out* in-situ LPBF process monitoring. While I understand this is hardware-architecture de-risking, optimizing solely on post-print hardness/density leaves a massive data vacuum regarding *why* a particular build failed (e.g., keyhole vs. lack-of-fusion porosity). The BOFN algorithm might struggle to efficiently navigate the latent parameter space using only terminal hardness/density as the objective function without thermal history or melt-pool dynamics to inform the surrogate model.

**What I would require before approving an EAGER request:**
A brief strategy on how the BOFN algorithm handles catastrophic build failures (e.g., severe lack of fusion that causes the recoater blade to crash, aborting the print). If the MX-100 crashes on cycle 4, how does the autonomous loop recover and update the Bayesian prior without human intervention?

**Likelihood I would champion this in my division:** High.
**Recommendation:** Approve with revisions.
**Confidence:** High.

---

## Khershed Cooper (Long-Tenure, AM Materials & Platforms)

**Why this would land on my desk:**
I have overseen CMMI advanced manufacturing and nanomanufacturing hardware platforms for years, particularly those involving multi-step synthesis and processing. I frequently handle proposals bridging computational materials science (CALPHAD) with physical metal AM processing. 

**What I like (after the revisions):**
The PI smartly addressed the powder bottleneck by explicitly bringing in the ultrasonic atomizer and defining a strict QC plan (PSD by laser diffraction, sphericity by SEM, O2 by inert-gas fusion). This gives credibility to the metallurgical side of the operation. The framing of this as "hardware-architecture de-risking" rather than a materials science campaign is politically astute—it justifies keeping this strictly within CMMI and avoiding a messy co-review with DMR, which would likely drag out the timeline and impose orthogonal basic-science requirements. The fallback plans (umbilicals, manual transfer) are practical.

**What still worries me:**
The integration of a $220K ultrasonic atomizer (even if operator-assisted) into a VLM environment alongside an LPBF machine and characterization equipment raises severe contamination and safety concerns. Aluminum fines are a Class D fire hazard. While the PI notes BYU EHS review is "handled outside this request," placing reactive metal powder generation, handling, and LPBF processing in close vertical proximity inside an enclosed lift module presents a non-trivial risk that a single spark could cause a catastrophic event.

**What I would require before approving an EAGER request:**
Confirmation that the VLM enclosure itself is inerted or structurally rated for Class D particulate mitigation, not just that the individual MX-100 has a sealed Ar atmosphere. If the atomizer is operator-assisted, I need to know how the powder is safely transferred *into* the autonomous loop without exposing the VLM environment to explosive dust.

**Likelihood I would champion this in my division:** Medium. (The concept is exciting, but the physical integration risks are substantial).
**Recommendation:** Approve with revisions.
**Confidence:** High.

---

## Andrew B. Wells (Hard Tech & Hardware Architecture)

**Why this would land on my desk:**
My focus is on hard tech, physical manufacturing infrastructure, and transitioning manufacturing technologies. A proposal explicitly pitching a scalable, replicable "$80K VLM + sub-$40K LPBF facility model" to rethink manufacturing footprint and autonomous integration is exactly the kind of systems-level engineering I support.

**What I like (after the revisions):**
This is a phenomenal use of the EAGER mechanism. The PI is asking for ~$300K to test a radical hardware hypothesis—that industrial warehousing tech (VLMs) can serve as the backbone for high-precision scientific automation at a fraction of the cost and footprint of traditional robotics labs. The go/no-go milestones are highly quantitative (±2 mm positioning, <50 µm vibration, 24h continuous operation), which makes it easy to measure success or failure at the end of Year 1. 

**What still worries me:**
The letters of collaboration (LoCs) are explicitly marked as placeholders. For a systems-integration project of this complexity, the PI needs airtight commitments from the robotics and computational collaborators (Killpack and Homer). Furthermore, relying on a startup-funded, newly acquired $220K atomizer introduces a dangerous external dependency. If the atomizer delivery is delayed or commissioning fails, the entire Year 2 custom alloy loop is paralyzed.

**What I would require before approving an EAGER request:**
1. The finalized, signed LoCs from the collaborators. 
2. A clear decoupling of the VLM hardware de-risking from the new atomizer timeline. The PI needs to state that if the atomizer is delayed, Year 2 will proceed using commercially purchased pre-alloyed powder to demonstrate the full loop.

**Likelihood I would champion this in my division:** High. 
**Recommendation:** Approve with revisions.
**Confidence:** High.

---

## Cross-PO Synthesis & Next Steps

**Lead-PO Digest**
The revised FLAIME-VCL concept outline is substantially stronger. By tightly defining the BOFN parameters, formalizing the powder QC, and rigorously outlining the spatial/vibrational metrology for the VLM, the PI has transformed a loosely defined "self-driving lab" pitch into a hard-nosed mechanical and systems engineering testbed. The explicit framing as CMMI-led hardware de-risking successfully inoculates the proposal against DMR mission creep.

**Convergent Concerns:**
All three POs are enthusiastic about the core premise but share a pragmatic anxiety about *edge cases and dependencies in physical integration*. When things go wrong in hardware—whether a recoater crash (Bian), a Class D powder spill (Cooper), or a delayed equipment delivery (Wells)—how robust is the proposed architecture? 

**Divergent Concerns:**
Bian views the project through a data lens, wanting to know how the BOFN survives lack-of-data or aborted prints. Cooper views it through a physical/metallurgical lens, worrying about cross-contamination and the proximity of reactive metal powders. Wells views it through a project management lens, focusing on partner commitments and critical-path dependencies.

**Net Recommendation:** Encourage submission of a full EAGER proposal, subject to one final high-leverage revision.

**The ONE highest-leverage next revision before a formal EAGER request goes in:**
The PI must add a **"System Fault & Dependency Resilience"** section (perhaps replacing or merging with the current risk mitigations). This section must explicitly address:
1. How the BOFN algorithm handles aborted/failed prints (data resilience).
2. How the physical VLM architecture isolates hazards, specifically reactive Al dust (physical resilience).
3. A commitment to use commercial powder for the Year 2 loop if the atomizer commissioning is delayed (schedule resilience). 

*Discretionary Analytical Decisions:*
*   *PO Selection*: Selected Bian, Cooper, and Wells based on verified current CMMI AM program officer listings, favoring them over the previous panel (Chou/Lewis) to reflect current 2024/2025 NSF staffing realities and provide a fresh set of complementary perspectives (Data/ML, Materials/Safety, Hard-Tech/Systems).
*   *Feedback Interpretation*: Treated the EAGER as a primarily hardware/systems engineering proposal, deliberately sidestepping deep materials science critiques based on the PI's explicit framing to exclude DMR.
*   *Safety Focus*: Amplified the safety/EHS critique (Class D fires) as a critical concern for a mechanical engineering PO evaluating a novel enclosed hardware platform, as this is a common failure point for academic metal AM integration.