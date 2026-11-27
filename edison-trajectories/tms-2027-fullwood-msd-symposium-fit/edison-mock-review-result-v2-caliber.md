# Edison Persona Mock-Review Result (v2) — TMS 2027 Fullwood MSD Symposium — FINAL CALIBER submission draft

**Task:** `72852aae-8245-4789-bf04-798d40705842` (`LITERATURE_HIGH`) · **Status:** success
**Verdict:** **SUBMIT** (confidence High, ~5–2 in favor) — upgraded from the v1 pre-reframe verdict of SUBMIT-IF-RETAILORED
**Reviewed:** the actual EBSD-forward, CALIBER-named Fullwood submission draft (title "Patterns First…"), role-played by all seven organizers (Johnson, Homer, Miles, Niezgoda, Knezevic, Kacher, Ruggles). @sgbaird holds an invited talk in this symposium.
**Prompt:** [`edison-prompt-v2-caliber-submission.md`](edison-prompt-v2-caliber-submission.md) · **v1 result (pre-reframe):** [`edison-mock-review-result.md`](edison-mock-review-result.md)

---

Question: # Edison LITERATURE_HIGH prompt (v2) — Fullwood MSD persona mock review of the FINAL CALIBER submission abstract

> **What's new vs. [`edison-prompt.md`](edison-prompt.md):** the first Fullwood panel reviewed the pre-reframe,
> generically-titled "Multi-Modal Characterization-Parameter Optimization" abstract. This v2 review is run on
> the **actual Fullwood-tailored submission draft** — the EBSD-forward, CALIBER-named, reframed version from
> [`../../tms-2027-compositional-analysis-abstract-fullwood.md`](../../tms-2027-compositional-analysis-abstract-fullwood.md).
> Requested by @sgbaird on PR #103 (he holds an invited talk in this symposium).

---

ROLE: You are a panel of seven TMS 2027 symposium organizers conducting a mock peer review of a submitted abstract. For each organizer, give feedback IN THEIR VOICE, grounded in their actual research expertise (summarized below), then converge on a committee recommendation. Use real literature (with DOIs/arXiv IDs) to support claims about EBSD/HR-EBSD, microstructure-sensitive design (MSD), statistical microstructure characterization, indexing/pattern-quality metrology, and AI/autonomous characterization.

THE SYMPOSIUM (TMS 2027; sponsored by the TMS Materials Processing & Manufacturing Division and Structural Materials Division; Advanced Characterization/Testing/Simulation, Computational Materials Science & Engineering, and Mechanical Behavior of Materials Committees):
"Microstructure-Sensitive Design and Advanced Characterization: An MPMD/SMD Symposium Honoring David T. Fullwood." Scope: honoring Prof. David T. Fullwood's contributions, emphasizing advanced characterization techniques and modeling to understand the link between a material's microstructure and its mechanical behavior. Core topics: (1) Microstructure-Sensitive Design (MSD) and statistical microstructure descriptions; (2) advanced electron-based characterization (EBSD, HR-EBSD techniques); (3) computational and experimental mechanics integration; (4) multiscale deformation analysis across atomic to macroscopic scales.

IMPORTANT CONTEXT: This is a **BYU-hosted, in-house-flavored symposium** honoring a BYU professor; three of the seven organizers are BYU Mechanical Engineering faculty. **The abstract under review is from the BYU Vertical Cloud Lab (BYU Mechanical Engineering) — i.e., the same department as the honoree and several organizers.** The submitting PI (Sterling Baird) also holds an invited talk in this same symposium. Weigh both scientific fit and the practical reality that this is a friendly home venue.

THE ORGANIZERS AND THEIR EXPERTISE (role-play each as a reviewer):
1. Oliver K. Johnson, Brigham Young University — microstructure/grain-boundary structure-property relationships; graph/network analysis; machine learning for microstructure; EBSD. BYU ME.
2. Eric R. Homer, Brigham Young University — grain-boundary structure, HR-EBSD, GND measurement, atomistics, ML representations of grain boundaries; co-directs the BYU Microstructure lab. BYU ME.
3. Michael P. Miles, Brigham Young University — friction-stir processing/welding, formability, EBSD, digital image correlation. BYU Manufacturing Engineering.
4. Stephen R. Niezgoda, Ohio State University — microstructure-sensitive design, texture, statistical microstructure descriptors, uncertainty quantification, ICME. Deep MSD lineage (Kalidindi/Adams/Fullwood school).
5. Marko Knezevic, University of New Hampshire — crystal plasticity, texture evolution, AM, multiscale modeling of deformation.
6. Josh Kacher, Georgia Institute of Technology — in-situ TEM deformation, EBSD, local chemistry effects on defects (dislocations, twins), multiscale defect characterization; co-author of "Thinking Microscopes" (agentic/autonomous microscopy).
7. Tim J. Ruggles, Sandia National Laboratories — HR-EBSD; cross-correlation EBSD for local stress and GND density; in-situ HR-EBSD + DIC; EBSD pattern-quality/indexing methodology.
(The honoree, David T. Fullwood, BYU — HR-EBSD, GND, MSD, spherical-harmonic microstructure representation — is the thematic anchor.)

THE ABSTRACT UNDER REVIEW (BYU Vertical Cloud Lab, FLAIME project — final Fullwood-tailored draft):

Title: "Patterns First: A Retrieval-Augmented, Uncertainty-Aware Platform (CALIBER) for High-Fidelity EBSD Acquisition to Enable Microstructure-Sensitive Design."

Abstract (149 words): "Trustworthy microstructure-sensitive design begins with trustworthy patterns: HR-EBSD elastic-strain and GND-density measurements, and the statistical microstructure descriptors they feed, are only as reliable as the upstream EBSD acquisition — yet that step is fragile and operator-dependent. On laser-powder-bed-fusion Al–Si, EBSD indexing yield rose from ~40% to ~77% of points above CI = 0.1 once beam current and a custom AlSi10Mg / diamond-cubic-Si phase model were corrected; standardless SEM-EDS separately over-reported trace Mg several-fold. We present CALIBER, an uncertainty-aware platform that recommends and iteratively refines EBSD — and complementary EDS/XRF — acquisition parameters for a given sample and analysis goal. Recommendations are grounded in retrieval over characterization standards and HR-EBSD literature, electron-beam and interaction-volume simulation, and a growing provenance-tracked dataset of parameter sweeps. The result is a reproducible, transferable route to high-quality patterns, and a labeled dataset for statistical microstructure quantification, that makes downstream HR-EBSD, GND, and MSD analyses defensible."

WHAT WE NEED FROM YOU:
A. FIT ASSESSMENT. Assess fit honestly for a symposium on MSD + advanced (EBSD/HR-EBSD) characterization honoring Fullwood. This draft has been deliberately reframed to lead with EBSD pattern-quality/indexing yield as the *upstream enabler* of HR-EBSD, GND, and statistical microstructure descriptors (Topic 2 + the "MSD" thread), with EDS/XRF/ICP demoted to supporting cast. Assess whether that reframe successfully moves it from "instrument informatics" into the room's science. Where is the overlap now genuinely strong, and where does a residual gap remain (it still does not itself compute GNDs, elastic strain, or property predictions — it enables them)? Did the "Patterns First" / "garbage patterns in → garbage MSD out" enabling framing land, or does it still read as tooling to a mechanics audience?
B. PER-ORGANIZER MOCK REVIEW. For each of the 7 organizers, 3–5 sentences in their voice: accept or reject, what specifically excites or bothers them about THIS reframed draft, and the single change that would most improve it for them. (Ruggles and Homer especially: does the "pattern quality is the prerequisite for reliable HR-EBSD strain/GND" argument serve the workflows they care about? Niezgoda: does the "labeled dataset for statistical microstructure quantification" hook connect to MSD descriptors credibly? Kacher: does CALIBER read as a concrete realization of the "Thinking Microscopes" agentic-microscopy vision?)
C. VERDICT. Committee-level recommendation: SUBMIT / SUBMIT-IF-RETAILORED / DO-NOT-SUBMIT, with confidence and the single biggest remaining risk. Compare explicitly to the prior panel's verdict on the un-reframed version (SUBMIT-IF-RETAILORED, confidence High, ~5–2 for): did this reframe move the needle toward a clean SUBMIT?
D. TAILORING PLAYBOOK. Concrete, prioritized edits to sharpen THIS draft further for this room — e.g., whether to add one explicit forward-looking mechanics sentence (validated EBSD → CPFE / DIC-EBSD / process–structure–property) to satisfy Knezevic; whether a before/after cross-correlation-quality figure is worth it; which specific citations to name-drop (the honoree's own HR-EBSD/GND work; Ram & De Graef dictionary indexing; Niezgoda/Kalidindi statistical descriptors; Kacher "Thinking Microscopes"). Ground in real literature (DOIs).
E. LITERATURE. Cite real, verifiable sources (DOIs/arXiv) on (i) EBSD indexing quality / pattern quality / dictionary indexing and beam-condition effects, (ii) HR-EBSD and GND measurement (Fullwood/Wilkinson lineage), and (iii) MSD and statistical microstructure characterization.

Return a well-structured report: one-paragraph executive summary with the bottom-line verdict at top, then sections A–E, with per-organizer subsections in B.


# Mock Peer Review: "Patterns First: A Retrieval-Augmented, Uncertainty-Aware Platform (CALIBER) for High-Fidelity EBSD Acquisition to Enable Microstructure-Sensitive Design"

## Executive Summary

**Bottom-line verdict: SUBMIT (confidence: High, ~5–2 for).** The Fullwood-tailored reframe of the CALIBER abstract has materially improved its fit for the "Microstructure-Sensitive Design and Advanced Characterization" symposium honoring David T. Fullwood. By leading with EBSD pattern quality and indexing yield as the upstream enabler of HR-EBSD elastic-strain mapping, GND density estimation, and statistical microstructure descriptors — and demoting EDS/XRF/ICP to supporting roles — the abstract now speaks directly to the symposium's core topics (kalidindi2006elasticpropertiesclosures pages 1-2, niezgoda2008delineationofthe pages 1-2, niezgoda2008delineationofthe pages 2-3). The "garbage patterns in → garbage MSD out" logic is scientifically sound and well-grounded: Hansen et al. (doi:10.1017/S1431927617000204) demonstrated that noise-generating factors in cross-correlation EBSD directly degrade GND measurements, and Britton & Wilkinson (doi:10.1016/j.ultramic.2013.08.005, doi:10.1016/j.ultramic.2013.08.006) showed that detector and acquisition conditions constrain HR-EBSD strain precision. The LPBF AlSi10Mg indexing challenge is validated in the literature: Snopiński et al. (doi:10.3390/sym17050709) confirm that Al/Si phase indexing is technically difficult due to diffraction-pattern similarity (snopinski2025theinfluenceof pages 6-9). The abstract's retrieval-augmented, provenance-tracked design aligns with Kacher's "Thinking Microscopes" agentic AI vision (jamali2026thinkingmicroscopesagentic pages 3-4, jamali2026thinkingmicroscopesagentic pages 1-2, jamali2026thinkingmicroscopesagentic pages 2-3). This represents a clean upgrade from the prior panel's SUBMIT-IF-RETAILORED verdict to a SUBMIT recommendation, with two remaining edits (add one forward-looking mechanics sentence; sharpen the MSD descriptor hook) that can be made at the talk stage. The single biggest remaining risk is that the abstract still does not itself compute any downstream quantity (no GNDs, no strain maps, no property predictions), which may leave the modeling half of the room wanting more — but for a 149-word abstract in a home-venue symposium, the enabling framing is now sufficient.

---

## A. FIT ASSESSMENT

### Where the overlap is now genuinely strong

The reframed abstract achieves strong alignment with three of the symposium's four core topics:

**1. Advanced electron-based characterization (Topic 2).** The abstract's central technical contribution — improving EBSD indexing yield from ~40% to ~77% CI > 0.1 on LPBF AlSi10Mg — is squarely within the room's expertise. The claim that acquisition quality is "fragile and operator-dependent" is well-supported by Randle (doi:10.1016/j.matchar.2009.05.011) and by the LPBF Al-Si phase-indexing difficulty confirmed by Snopiński et al. (snopinski2025theinfluenceof pages 6-9). The explicit mention of HR-EBSD, cross-correlation quality, and GND density as downstream beneficiaries connects directly to Fullwood's own research lineage (doi:10.1016/j.ultramic.2013.04.011, doi:10.1016/j.matchar.2015.07.017).

**2. MSD and statistical microstructure descriptions (Topic 1).** The abstract explicitly frames its output as "a labeled dataset for statistical microstructure quantification, that makes downstream HR-EBSD, GND, and MSD analyses defensible." This connects to the Kalidindi/Adams/Fullwood MSD framework that uses spectral representations of 2-point correlation functions to establish invertible structure–property linkages (kalidindi2006elasticpropertiesclosures pages 1-2, niezgoda2008delineationofthe pages 1-2, niezgoda2008delineationofthe pages 2-3). The microstructure quantification framework developed by Niezgoda et al. (doi:10.1186/2193-9772-2-3) — which underpins the symposium's intellectual lineage — requires precisely the kind of high-fidelity, well-labeled EBSD data that CALIBER aims to produce (niezgoda2013novelmicrostructurequantification pages 2-4, niezgoda2013novelmicrostructurequantification pages 1-2).

**3. Computational and experimental integration (Topic 3).** CALIBER's retrieval-augmented, simulation-informed approach (electron-beam and interaction-volume modeling) bridges computational prediction with experimental characterization, fitting the symposium's emphasis on integration.

### Where a residual gap remains

**Multiscale deformation analysis (Topic 4) and mechanics.** The abstract still does not itself compute GNDs, elastic strains, or property predictions. It enables them. For a pure mechanics audience — Knezevic's crystal-plasticity world, for instance, where EBSD data directly feed CPFE simulations (feather2021anumericalstudy pages 2-3) — the abstract reads as upstream infrastructure rather than science. This is an honest characterization: CALIBER is an acquisition-optimization platform, not a constitutive model. The "Patterns First" framing successfully argues *why* this matters to mechanics, but it does not *do* mechanics.

### Did the reframe land?

Yes, substantially. The prior version ("Multi-Modal Characterization-Parameter Optimization") read as generic instrument informatics. This version leads with the scientific claim that "trustworthy MSD begins with trustworthy patterns" and explicitly names the downstream workflows (HR-EBSD, GND, MSD) that the symposium exists to discuss. The "Patterns First" framing converts the work from tooling into an upstream prerequisite argument that the room's practitioners will recognize from their own experience — anyone who has spent a day fighting EBSD beam conditions on a difficult alloy will nod. The residual risk is that nodding is not the same as being excited: a mechanics audience may still want to see the patterns actually *used* for something.

---

## B. PER-ORGANIZER MOCK REVIEWS

The following table summarizes each organizer's likely stance:

| Organizer | Affiliation | Core Expertise | Individual Verdict | Key Concern | Single Most Important Edit |
|---|---|---|---|---|---|
| Oliver K. Johnson | Brigham Young University | Microstructure and grain-boundary networks; ML for microstructure; EBSD | Soft Accept | The reframed abstract now fits the EBSD/MSD room better, but it still stops short of connecting improved acquisition to grain-boundary-network statistics or related descriptors that EBSD maps actually feed downstream. This matters especially given Johnson’s work on graph/spectral representations of GB networks and structure–property inference (owens2025featureengineeringdescriptors pages 16-17). | Add one explicit downstream example such as grain-boundary character distribution or grain-boundary network statistics enabled by higher-fidelity indexing. |
| Eric R. Homer | Brigham Young University | Grain-boundary structure; HR-EBSD; GND; ML for grain boundaries | Accept | The “patterns first” framing lands well because HR-EBSD elastic strain and GND estimates are highly sensitive to upstream pattern noise and acquisition quality, so better patterns are not peripheral tooling but a direct prerequisite for defensible measurements (doi:10.1017/S1431927617000204; doi:10.1016/j.ultramic.2013.04.011). | Cite Hansen et al. on noise-generating factors in cross-correlation EBSD to strengthen the argument. |
| Michael P. Miles | Brigham Young University | Friction-stir processing; formability; EBSD; DIC | Soft Accept | The practical characterization angle is interesting and the LPBF Al–Si example is relevant, but the draft still underplays how this improves workflows that combine EBSD with deformation validation, especially DIC-linked studies. | Add a brief downstream validation sentence linking improved EBSD acquisition to DIC-EBSD correlation or deformation mapping workflows. |
| Stephen R. Niezgoda | Ohio State University | Microstructure-sensitive design; texture; statistical descriptors; uncertainty quantification | Borderline Accept | The phrase “labeled dataset for statistical microstructure quantification” is promising, but it remains underspecified: the abstract does not yet say what descriptors the data enable or how the acquisition/provenance stack becomes an MSD-ready n-point-statistics pipeline (kalidindi2006elasticpropertiesclosures pages 1-2, niezgoda2008delineationofthe pages 1-2, niezgoda2013novelmicrostructurequantification pages 22-23, niezgoda2013novelmicrostructurequantification pages 7-9). | Specify which statistical descriptors the labeled data support, e.g., orientation distributions, two-point correlations, texture/phase fields, or other n-point statistics for MSD. |
| Marko Knezevic | University of New Hampshire | Crystal plasticity; texture evolution; additive manufacturing; multiscale deformation modeling | Borderline Accept | The abstract is much better aligned than the pre-reframe, but for a mechanics/modeling audience it still reads primarily as an enabling characterization platform because it never explicitly closes the loop to CPFE, texture-informed constitutive modeling, or process–structure–property prediction (feather2021anumericalstudy pages 2-3). | Add one forward-looking sentence tying validated EBSD data to CPFE, texture-based simulations, or broader process–structure–property workflows. |
| Josh Kacher | Georgia Institute of Technology | In-situ TEM deformation; EBSD; multiscale defect characterization; autonomous microscopy | Accept | CALIBER reads as a concrete, materials-characterization-side realization of the agentic microscopy infrastructure Kacher has argued for: retrieval over literature/standards, iterative refinement, provenance tracking, and multimodal acquisition recommendations all align with the “Thinking Microscopes” vision for closed-loop experimental design (jamali2026thinkingmicroscopesagentic pages 3-4, jamali2026thinkingmicroscopesagentic pages 1-2, jamali2026thinkingmicroscopesagentic pages 2-3, jamali2026thinkingmicroscopesagentic pages 4-5). | Position CALIBER explicitly as an agentic experimental-design or characterization-planning agent rather than only as a recommendation platform. |
| Tim J. Ruggles | Sandia National Laboratories | HR-EBSD; cross-correlation EBSD; GND density; in-situ HR-EBSD + DIC; pattern-quality methodology | Accept | The “garbage patterns in, garbage MSD/HR-EBSD out” logic is exactly right for HR-EBSD workflows because cross-correlation quality, local stress inference, and bulk GND estimates depend on stable, high-fidelity patterns; this is a genuine upstream scientific issue, not mere instrument tuning (doi:10.1016/j.ultramic.2013.04.011; doi:10.1093/mam/ozaf130). | Include a before/after cross-correlation quality metric or analogous HR-EBSD-relevant figure of merit, not just indexing yield. |


*Table: This table summarizes the likely stance of each symposium organizer on the CALIBER abstract after the Fullwood-tailored reframe. It highlights where the abstract now fits strongly and what single edit would most improve acceptance for each reviewer persona.*

### B.1 Oliver K. Johnson (BYU)

*"I know Sterling well — we've co-authored together on grain-boundary structure–property inference using polycrystalline EBSD data (doi:10.1016/j.actamat.2021.116769, doi:10.1007/s10853-019-04125-z). The reframe is a real improvement: leading with EBSD indexing yield and pattern quality puts the abstract in our characterization wheelhouse, and the provenance-tracked dataset idea resonates with my interest in systematic microstructure representations. What I'd still like to see is one explicit mention of how better indexing feeds grain-boundary character distributions or grain-boundary network statistics — the kind of descriptors that feed my spectral graph theory work (doi:10.1016/j.actamat.2017.11.054) and that David cares about. The abstract says 'statistical microstructure quantification' generically; specifying even one concrete descriptor class would strengthen the MSD hook. I'd vote soft accept — it fits the room, and Sterling has an invited talk here, which tells me we already endorsed the research direction."*

### B.2 Eric R. Homer (BYU)

*"The 'patterns first' argument is exactly right. My lab does HR-EBSD and GND mapping routinely, and we published explicitly on how noise-generating factors in cross-correlation EBSD propagate into GND estimates (Hansen et al., doi:10.1017/S1431927617000204 — David and I are both on that paper). Pattern quality is not peripheral: it is the rate-limiting upstream variable for everything we measure. I'm genuinely interested in CALIBER's approach to recommending beam current and phase models, because those are precisely the knobs we fight with on new alloy systems. The AlSi10Mg example is compelling because that Al/Si diffraction-pattern similarity is a known headache. My one suggestion: explicitly cite our noise paper to anchor the 'patterns first' claim in the literature David's group produced. Accept."*

### B.3 Michael P. Miles (BYU)

*"As someone who uses EBSD alongside DIC for formability and friction-stir processing studies, I appreciate the practical focus on getting acquisition right before analysis. The LPBF Al-Si case study is relevant to manufacturing, and the CI improvement from 40% to 77% is a tangible result that any EBSD user would value. My concern is that the abstract doesn't connect to deformation-based validation — I'd like to see one sentence noting that high-quality EBSD enables robust DIC-EBSD correlation or strain-mapping workflows. It's a minor gap, and given that this is a home-venue submission from BYU ME, I'd vote soft accept. The single edit: mention DIC-EBSD or in-situ deformation mapping as a downstream application to connect with the experimental mechanics thread."*

### B.4 Stephen R. Niezgoda (Ohio State)

*"I helped build the mathematical framework for MSD with David, Brent Adams, and Surya Kalidindi. Our 2-point correlation work (doi:10.1016/j.actamat.2008.07.005) and microstructure quantification framework (doi:10.1186/2193-9772-2-3) are precisely what the abstract's 'labeled dataset for statistical microstructure quantification' phrase is pointing at — but it's pointing, not connecting (niezgoda2013novelmicrostructurequantification pages 2-4, niezgoda2013novelmicrostructurequantification pages 1-2). What statistical descriptors? Orientation distribution functions? 2-point spatial correlations? Phase fraction fields? The abstract needs to say. Without that specificity, the MSD hook reads as a marketing tag rather than a scientific claim. I also note that the phrase 'uncertainty-aware' is used without specifying what uncertainty is quantified — is it indexing confidence, or is there a Bayesian posterior over orientation assignments? The Niezgoda/Kalidindi stochastic-process representation of microstructure (doi:10.1016/j.actamat.2011.06.051) treats microstructure variance rigorously; CALIBER should clarify how its uncertainty maps onto that framework. I'd vote borderline accept — the topic is relevant but the MSD connection is underdeveloped."* (niezgoda2013novelmicrostructurequantification pages 22-23, niezgoda2013novelmicrostructurequantification pages 4-7, niezgoda2013novelmicrostructurequantification pages 7-9)

### B.5 Marko Knezevic (UNH)

*"I've used EBSD data as direct inputs for crystal plasticity finite element simulations throughout my career — from texture-based MSD closures with Kalidindi (doi:10.1016/j.commatsci.2006.08.025) to explicit-grain-structure CPFE (doi:10.1007/s00466-020-01918-x). When I read this abstract, I see an acquisition platform that produces better EBSD maps. Fine. But the abstract never closes the loop: it doesn't say that the validated maps feed CPFE, or inform process–structure–property predictions, or enable in-situ HR-EBSD / DIC comparison with crystal plasticity predictions. For a symposium that integrates characterization with mechanical behavior modeling, this is a gap (feather2021anumericalstudy pages 2-3). The single most important edit is one forward-looking sentence: 'The resulting high-fidelity EBSD datasets provide the grain morphology, orientation, and phase inputs required for crystal plasticity modeling and process–structure–property optimization of AM alloys.' That costs 20 words and buys this abstract into the modeling half of the room. Without it, I'm borderline accept — with it, I'm a yes."*

### B.6 Josh Kacher (Georgia Tech)

*"CALIBER reads to me as a concrete, materials-characterization-side realization of the agentic experimental-design infrastructure we've been arguing for. In our 'Thinking Microscopes' paper (doi:10.1038/s41524-026-02077-y), we called for specialized AI agents that synthesize literature, lab notebooks, and prior experimental metadata to develop optimized experimental protocols — and that's essentially what CALIBER does for EBSD/EDS acquisition (jamali2026thinkingmicroscopesagentic pages 3-4, jamali2026thinkingmicroscopesagentic pages 1-2). The retrieval-augmented grounding in characterization standards and HR-EBSD literature, the iterative refinement loop, and the provenance-tracked parameter-sweep dataset all map directly onto our framework's requirements for centralized data repositories and standardized, interoperable experimental records (jamali2026thinkingmicroscopesagentic pages 4-5). I'd encourage the authors to position CALIBER explicitly as an 'agentic experimental-design agent' rather than just a 'platform that recommends' — the language matters for this community. My one concern: CALIBER is currently pre-instrument (it recommends parameters rather than controlling the microscope in a closed loop), which places it earlier in the autonomy spectrum than what we envision. But as an experimental-design agent, it's exactly the right first step. Accept."*

### B.7 Tim J. Ruggles (Sandia)

*"Pattern quality is my scientific bread and butter. My work with David on bulk GND estimation (doi:10.1016/j.ultramic.2013.04.011) and our more recent concurrent in-situ HR-EBSD + DIC work (doi:10.1093/mam/ozaf130) both depend on starting with high-quality, properly acquired Kikuchi patterns. The abstract's core claim — that cross-correlation EBSD measurements of elastic strain and GND density are only as reliable as the upstream acquisition — is not just true, it's underappreciated in the community. Every time someone publishes a GND map without reporting their beam current, step size, or pattern-averaging scheme, they're hiding the most important variable. CALIBER's approach to systematizing and tracking these parameters is exactly what the field needs. My one edit: the abstract reports indexing yield (CI > 0.1) as the quality metric, but for HR-EBSD the relevant metric is cross-correlation peak quality, not Hough-based confidence index. If they could show a before/after improvement in cross-correlation sharpness or strain-field noise floor, that would speak directly to the HR-EBSD community. Accept."*

---

## C. VERDICT

**Committee-level recommendation: SUBMIT**

**Confidence: High (~5–2 for).** Four organizers (Homer, Kacher, Ruggles, and Johnson leaning) vote accept or strong soft-accept; Miles leans soft-accept on pragmatic/home-venue grounds; Niezgoda and Knezevic are borderline but persuadable. No reviewer recommends reject.

**Comparison to prior panel verdict:** The v1 panel rated the un-reframed "Multi-Modal Characterization-Parameter Optimization" abstract as SUBMIT-IF-RETAILORED (High confidence, ~5–2 for). This Fullwood-tailored reframe has moved the needle from conditional to clean SUBMIT. The key improvements that drove this upgrade:

1. **EBSD-forward framing** replaced generic "multi-modal characterization" language with the specific upstream–downstream argument that resonates with the HR-EBSD/GND community.
2. **"Patterns First" + "garbage in → garbage out" logic** converted the abstract from instrument informatics into a scientific claim about measurement validity.
3. **Explicit naming of HR-EBSD, GND, and MSD** as downstream beneficiaries connects to Fullwood's own research legacy.
4. **The CALIBER acronym** gives the platform a memorable identity and implicitly signals maturity.

**Single biggest remaining risk:** The abstract is still an *enabler* abstract — it does not itself compute any mechanical quantity or demonstrate a structure–property prediction. If the talk itself shows the enabled downstream analysis (even preliminary GND maps or orientation distributions from the improved data), this risk dissolves. If the talk is purely about acquisition tuning, it may underwhelm the modeling half of the room.

---

## D. TAILORING PLAYBOOK

### Priority 1: Add one forward-looking mechanics sentence (HIGH IMPACT, LOW COST)

Replace the final clause or append: *"…making downstream HR-EBSD, GND, and MSD analyses defensible, and providing the grain morphology, orientation, and phase inputs needed for crystal plasticity simulation and process–structure–property optimization of AM alloys."* This costs ~20 words and directly addresses Knezevic's concern, converts his borderline to an accept, and connects to the CPFE workflow where EBSD data feed DREAM.3D → finite-element meshes (feather2021anumericalstudy pages 2-3). Cite Feather, Lim, & Knezevic (doi:10.1007/s00466-020-01918-x) in the talk.

### Priority 2: Sharpen the MSD descriptor hook (MEDIUM IMPACT)

Replace "a labeled dataset for statistical microstructure quantification" with something like "a provenance-tracked dataset of orientation distributions, phase fractions, and indexed grain maps suitable for 2-point statistics and MSD property closures." This addresses Niezgoda's concern that the MSD language is aspirational rather than specific (niezgoda2013novelmicrostructurequantification pages 22-23, niezgoda2013novelmicrostructurequantification pages 7-9, niezgoda2013novelmicrostructurequantification pages 23-25).

### Priority 3: Name-drop key citations (MEDIUM IMPACT, for the talk/extended abstract)

- **Fullwood (the honoree):** Cite Ruggles & Fullwood (doi:10.1016/j.ultramic.2013.04.011) and Hansen, Fullwood, Homer et al. (doi:10.1017/S1431927617000204) for the "pattern quality → GND quality" chain. Cite Kalidindi & Fullwood (doi:10.1007/s11837-007-0112-6) for the MSD spectral methods connection.
- **Ram & De Graef dictionary indexing:** Cite doi:10.1016/j.actamat.2017.10.069 for the multi-phase indexing challenge and as a methodological anchor for CALIBER's phase-model recommendations.
- **Niezgoda/Kalidindi statistical descriptors:** Cite doi:10.1016/j.actamat.2008.07.005 and doi:10.1186/2193-9772-2-3 for the MSD quantification framework.
- **Kacher "Thinking Microscopes":** Cite doi:10.1038/s41524-026-02077-y to position CALIBER in the emerging agentic-microscopy landscape (jamali2026thinkingmicroscopesagentic pages 3-4, jamali2026thinkingmicroscopesagentic pages 1-2).
- **Johnson spectral graph theory for GB networks:** Cite doi:10.1016/j.actamat.2017.11.054 to show how improved EBSD feeds higher-order grain-boundary descriptors.

### Priority 4: Consider a before/after cross-correlation quality figure (for the talk)

Ruggles notes that CI > 0.1 is a Hough-indexing metric, not an HR-EBSD metric. If the authors can show a before/after improvement in cross-correlation peak sharpness (or a reduction in strain-noise floor from, e.g., 2×10⁻⁴ to 5×10⁻⁵), that would convert the abstract's claim from "better indexing yield" to "better HR-EBSD quality," which is a much stronger argument for this audience.

### Priority 5: Position CALIBER as an agentic agent (LANGUAGE EDIT)

Per Kacher's feedback: change "platform that recommends" language to "agentic experimental-design agent" or "characterization-planning agent" where natural. This costs nothing and aligns with the Thinking Microscopes framing that resonates with the autonomy/AI thread (jamali2026thinkingmicroscopesagentic pages 2-3, jamali2026thinkingmicroscopesagentic pages 4-5).

---

## E. LITERATURE

The following table organizes verified references across the three requested domains:

| Section | Reference (Author et al., Year) | Topic | DOI | Relevance to Abstract |
|---|---|---|---|---|
| EBSD indexing / pattern quality | Ram & De Graef, 2018 | Phase differentiation by EBSD dictionary indexing | 10.1016/j.actamat.2017.10.069 | Directly relevant to multi-phase indexing challenges in LPBF AlSi10Mg and supports the abstract’s emphasis on improved phase models for higher-fidelity indexing. |
| EBSD indexing / pattern quality | Ram et al., 2017 | Error analysis of dictionary-approach EBSD indexing | 10.1016/j.ultramic.2017.04.016 | Supports the uncertainty-aware framing by showing that indexing quality should be quantified, not assumed. |
| EBSD indexing / pattern quality | Jackson et al., 2019 | Dictionary indexing tutorial for EBSD | 10.1007/s40192-019-00137-4 | Useful methodological anchor for framing CALIBER as literature-grounded acquisition and indexing support. |
| EBSD indexing / pattern quality | Rowenhorst et al., 2024 | Fast Radon transforms for high-precision EBSD orientation determination (pyEBSDindex) | 10.1107/S1600576723010221 | Demonstrates the modern move toward higher-throughput, more precise, and more automated EBSD indexing workflows. |
| EBSD indexing / pattern quality | Randle, 2009 | Strategies for reliable EBSD acquisition and processing | 10.1016/j.matchar.2009.05.011 | Classic best-practices citation for the claim that acquisition quality is fragile and operator-dependent. |
| EBSD indexing / pattern quality | Andrews et al., 2023 | Denoising autoencoder for improved Kikuchi pattern quality and indexing | 10.1016/j.ultramic.2023.113810 | Connects CALIBER to AI-assisted pattern-quality improvement rather than generic instrument informatics. |
| EBSD indexing / pattern quality | Snopiński et al., 2025 | EBSD characterization challenges in LPBF AlSi10Mg | 10.3390/sym17050709 | Confirms that Al/Si phase indexing is genuinely difficult in this alloy system, validating the motivating use case (snopinski2025theinfluenceof pages 6-9). |
| HR-EBSD / GND | Hansen et al., 2017 | Influence of noise-generating factors on cross-correlation EBSD measurement of GNDs | 10.1017/S1431927617000204 | Strongest direct support for the “patterns first” thesis: noise and acquisition conditions materially affect downstream GND inference. |
| HR-EBSD / GND | Ruggles & Fullwood, 2013 | Estimation of bulk GND density using HR-EBSD | 10.1016/j.ultramic.2013.04.011 | Foundational Fullwood/Ruggles citation linking pattern fidelity to defensible GND density measurement. |
| HR-EBSD / GND | Fullwood et al., 2015 | Validation of kinematically simulated pattern HR-EBSD for absolute strain and tetragonality | 10.1016/j.matchar.2015.07.017 | Supports the abstract’s argument that upstream pattern quality governs trustworthy HR-EBSD strain results. |
| HR-EBSD / GND | Hansen et al., 2023 | Character and distribution of GNDs in polycrystalline tantalum | 10.1093/micmic/ozad049 | Recent example from the Fullwood/Homer lineage showing why robust acquisition matters for spatially resolved GND mapping. |
| HR-EBSD / GND | Britton et al., 2013 | Precision of strain measurements using EBSD, Part 1: detector assessment | 10.1016/j.ultramic.2013.08.005 | Precision study from the Wilkinson lineage showing hardware and signal quality constraints on HR-EBSD strain metrology. |
| HR-EBSD / GND | Britton et al., 2013 | Precision of strain measurements using EBSD, Part 2: experimental demonstration | 10.1016/j.ultramic.2013.08.006 | Complements Part 1 and supports the claim that acquisition details propagate into measurement precision. |
| HR-EBSD / GND | Gilliland et al., 2026 | Concurrent in situ HR-EBSD and DIC for full-field stress-strain | 10.1093/mam/ozaf130 | Shows the exact sort of downstream workflow CALIBER could enable more defensibly through better upstream EBSD acquisition. |
| MSD / statistical microstructure | Niezgoda et al., 2013 | Microstructure quantification framework for databasing, visualization, and analysis | 10.1186/2193-9772-2-3 | Best citation for the abstract’s “labeled dataset for statistical microstructure quantification” claim and MSD-ready databasing (niezgoda2013novelmicrostructurequantification pages 2-4, niezgoda2013novelmicrostructurequantification pages 1-2). |
| MSD / statistical microstructure | Niezgoda, Fullwood, & Kalidindi, 2008 | Delineation of the space of 2-point correlations | 10.1016/j.actamat.2008.07.005 | Foundational Fullwood-linked MSD citation connecting statistical descriptors to invertible structure–property linkages (niezgoda2008delineationofthe pages 1-2, niezgoda2008delineationofthe pages 2-3). |
| MSD / statistical microstructure | Kalidindi, Fullwood, & Adams, 2006 | Elastic property closures using second-order homogenization theories | 10.1016/j.actamat.2006.03.005 | Canonical MSD citation showing how statistical microstructure descriptions feed property closures (kalidindi2006elasticpropertiesclosures pages 1-2). |
| MSD / statistical microstructure | Kalidindi & Fullwood, 2007 | Spectral methods for microstructure design | 10.1007/s11837-007-0112-6 | Honors the symposium’s Fullwood anchor and supports the MSD framing behind the abstract’s downstream ambitions. |
| MSD / statistical microstructure | Niezgoda et al., 2011 | Understanding and visualizing microstructure and microstructure variance as a stochastic process | 10.1016/j.actamat.2011.06.051 | Supports the uncertainty-aware and statistical-descriptor language in the abstract. |
| MSD / statistical microstructure | Johnson et al., 2018 | Spectral graph theory for characterization and homogenization of grain boundary networks | 10.1016/j.actamat.2017.11.054 | Provides a BYU/Fullwood-adjacent example of how improved EBSD maps can feed higher-order grain-boundary-network descriptors. |
| MSD / statistical microstructure | Jamali, Aghazadeh, & Kacher, 2026 | Thinking microscopes: agentic AI and the future of electron microscopy | 10.1038/s41524-026-02077-y | Frames CALIBER as a concrete step toward agentic, provenance-aware, closed-loop characterization infrastructure (jamali2026thinkingmicroscopesagentic pages 3-4, jamali2026thinkingmicroscopesagentic pages 4-5). |


*Table: This table organizes the key literature the mock review can cite across EBSD acquisition/indexing, HR-EBSD/GND metrology, and MSD/statistical microstructure characterization. It is useful for both substantiating the fit assessment and sharpening the tailoring recommendations with real, relevant references.*

### (i) EBSD Indexing Quality, Pattern Quality, Dictionary Indexing, and Beam-Condition Effects

- **Ram & De Graef (2018).** Phase differentiation by EBSD using dictionary indexing. *Acta Materialia* 144:352–364. doi:10.1016/j.actamat.2017.10.069. Directly relevant to the multi-phase (Al + diamond-cubic Si) indexing challenge in the abstract's AlSi10Mg use case.
- **Ram, Wright, Singh, & De Graef (2017).** Error analysis of crystal orientations obtained by the dictionary approach to EBSD indexing. *Ultramicroscopy* 181:17–26. doi:10.1016/j.ultramic.2017.04.016. Supports the uncertainty-aware framing by quantifying orientation-determination errors.
- **Jackson, Pascal, & De Graef (2019).** Dictionary indexing of EBSD patterns: a hands-on tutorial. *IMMI* 8:226–246. doi:10.1007/s40192-019-00137-4. Foundational DI methodology reference.
- **Rowenhorst, Callahan, & Ånes (2024).** Fast Radon transforms for high-precision EBSD orientation determination using pyEBSDindex. *J. Appl. Crystallogr.* 57:3–19. doi:10.1107/S1600576723010221. Modern automated indexing infrastructure.
- **Randle (2009).** Electron backscatter diffraction: strategies for reliable data acquisition and processing. *Mater. Charact.* 60:913–922. doi:10.1016/j.matchar.2009.05.011. Classic reference for the claim that EBSD quality is fragile and operator-dependent.
- **Andrews et al. (2023).** A denoising autoencoder for improved Kikuchi pattern quality and indexing. *Ultramicroscopy* 253:113810. doi:10.1016/j.ultramic.2023.113810. AI-assisted pattern improvement — connects CALIBER to the ML-for-characterization thread.
- **Snopiński et al. (2025).** Grain structure and mechanical properties of LPBF AlSi10Mg. *Symmetry* 17:709. doi:10.3390/sym17050709. Confirms that EBSD indexing of the Si phase in AlSi10Mg is technically challenging due to Al/Si diffraction-pattern similarity (snopinski2025theinfluenceof pages 6-9).

### (ii) HR-EBSD and GND Measurement (Fullwood/Wilkinson Lineage)

- **Hansen, Jackson, Fullwood, Wright, De Graef, Homer, & Wagoner (2017).** Influence of noise-generating factors on cross-correlation EBSD measurement of GNDs. *Microsc. Microanal.* 23:460–471. doi:10.1017/S1431927617000204. The single strongest citation supporting the "patterns first" thesis — demonstrates that noise and acquisition conditions materially affect GND inference. Co-authored by Fullwood and Homer.
- **Ruggles & Fullwood (2013).** Estimations of bulk geometrically necessary dislocation density using high resolution EBSD. *Ultramicroscopy* 133:8–15. doi:10.1016/j.ultramic.2013.04.011. Foundational Fullwood/Ruggles paper directly linking HR-EBSD pattern fidelity to defensible GND measurement.
- **Fullwood, Vaudin, Daniels, Ruggles, & Wright (2015).** Validation of kinematically simulated pattern HR-EBSD for measuring absolute strains and lattice tetragonality. *Mater. Charact.* 107:270–277. doi:10.1016/j.matchar.2015.07.017. Fullwood's validation of HR-EBSD strain measurement methodology.
- **Hansen, Carroll, Homer, Zhou, & Fullwood (2023).** Character and distribution of GNDs in polycrystalline tantalum. *Microsc. Microanal.* 29:953–966. doi:10.1093/micmic/ozad049. Recent Fullwood/Homer GND characterization.
- **Britton, Jiang, Clough, Tarleton, Kirkland, & Wilkinson (2013).** Assessing the precision of strain measurements using EBSD — Part 1: Detector assessment. *Ultramicroscopy* 135:126–135. doi:10.1016/j.ultramic.2013.08.005. Wilkinson-lineage precision study.
- **Britton et al. (2013).** Part 2: Experimental demonstration. *Ultramicroscopy* 135:136–141. doi:10.1016/j.ultramic.2013.08.006.
- **Gilliland, Ruggles, Fitzgerald, Carroll, Bomarito, & Hochhalter (2026).** Concurrent in situ HR-EBSD and DIC for full-field stress-strain. *Microsc. Microanal.* doi:10.1093/mam/ozaf130. Ruggles' state-of-the-art concurrent HR-EBSD + DIC work — exactly the downstream workflow CALIBER enables.

### (iii) MSD and Statistical Microstructure Characterization

- **Kalidindi, Binci, Fullwood, & Adams (2006).** Elastic properties closures using second-order homogenization theories. *Acta Materialia* 54:3117–3126. doi:10.1016/j.actamat.2006.03.005. Foundational MSD paper with Fullwood establishing spectral microstructure representations (kalidindi2006elasticpropertiesclosures pages 1-2).
- **Niezgoda, Fullwood, & Kalidindi (2008).** Delineation of the space of 2-point correlations in a composite material system. *Acta Materialia* 56:5285–5292. doi:10.1016/j.actamat.2008.07.005. Core MSD theory with Fullwood on 2-point correlation hulls (niezgoda2008delineationofthe pages 1-2, niezgoda2008delineationofthe pages 2-3).
- **Kalidindi & Fullwood (2007).** Spectral methods for microstructure design. *JOM* 59:26–31. doi:10.1007/s11837-007-0112-6. Key Fullwood MSD reference.
- **Niezgoda, Kanjarla, & Kalidindi (2013).** Novel microstructure quantification framework for databasing, visualization, and analysis. *IMMI* 2:54–80. doi:10.1186/2193-9772-2-3. Directly supports the abstract's "labeled dataset for statistical microstructure quantification" claim (niezgoda2013novelmicrostructurequantification pages 2-4, niezgoda2013novelmicrostructurequantification pages 1-2).
- **Niezgoda, Yabansu, & Kalidindi (2011).** Understanding and visualizing microstructure and microstructure variance as a stochastic process. *Acta Materialia* 59:6387–6400. doi:10.1016/j.actamat.2011.06.051. Supports uncertainty-aware statistical characterization.
- **Johnson et al. (2018).** Spectral graph theory for characterization and homogenization of grain boundary networks. *Acta Materialia* 146:42–54. doi:10.1016/j.actamat.2017.11.054. BYU/Johnson work showing how improved EBSD maps enable higher-order GB-network descriptors.
- **Jamali, Aghazadeh, & Kacher (2026).** Thinking microscopes: agentic AI and the future of electron microscopy. *npj Computational Materials* 12. doi:10.1038/s41524-026-02077-y. Frames CALIBER as a concrete realization of the agentic-microscopy vision (jamali2026thinkingmicroscopesagentic pages 3-4, jamali2026thinkingmicroscopesagentic pages 1-2, jamali2026thinkingmicroscopesagentic pages 2-3, jamali2026thinkingmicroscopesagentic pages 4-5, jamali2026thinkingmicroscopesagentic pages 5-6).
- **Feather, Lim, & Knezevic (2021).** A numerical study into element type and mesh resolution for CPFE modeling of explicit grain structures. *Computational Mechanics* 67:33–55. doi:10.1007/s00466-020-01918-x. Shows the EBSD → CPFE workflow that CALIBER's improved data feeds (feather2021anumericalstudy pages 2-3).
- **Owens, Mathew, Olaveson, Tavenner, Kober, Tucker, Hart, & Homer (2025).** Feature engineering descriptors, transforms, and ML for grain boundaries and variable-sized atom clusters. *npj Computational Materials* 11. doi:10.1038/s41524-024-01509-x. Homer's ML-for-GB work showing how atomic-scale descriptors enable GB property prediction (owens2025featureengineeringdescriptors pages 16-17, owens2025featureengineeringdescriptors pages 15-16).

References

1. (kalidindi2006elasticpropertiesclosures pages 1-2): Surya R. Kalidindi, Massimiliano Binci, David Fullwood, and Brent L. Adams. Elastic properties closures using second-order homogenization theories: case studies in composites of two isotropic constituents. Acta Materialia, 54:3117-3126, Jun 2006. URL: https://doi.org/10.1016/j.actamat.2006.03.005, doi:10.1016/j.actamat.2006.03.005. This article has 86 citations and is from a highest quality peer-reviewed journal.

2. (niezgoda2008delineationofthe pages 1-2): S.R. Niezgoda, D.T. Fullwood, and S.R. Kalidindi. Delineation of the space of 2-point correlations in a composite material system. Acta Materialia, 56:5285-5292, Oct 2008. URL: https://doi.org/10.1016/j.actamat.2008.07.005, doi:10.1016/j.actamat.2008.07.005. This article has 187 citations and is from a highest quality peer-reviewed journal.

3. (niezgoda2008delineationofthe pages 2-3): S.R. Niezgoda, D.T. Fullwood, and S.R. Kalidindi. Delineation of the space of 2-point correlations in a composite material system. Acta Materialia, 56:5285-5292, Oct 2008. URL: https://doi.org/10.1016/j.actamat.2008.07.005, doi:10.1016/j.actamat.2008.07.005. This article has 187 citations and is from a highest quality peer-reviewed journal.

4. (snopinski2025theinfluenceof pages 6-9): Przemysław Snopiński, Paweł Ostachowski, Krzysztof Matus, and Krzysztof Żaba. The influence of grain structure on mechanical properties of lpbf alsi10mg alloy obtained via conventional and kobo extrusion process. Symmetry, 17:709, May 2025. URL: https://doi.org/10.3390/sym17050709, doi:10.3390/sym17050709. This article has 1 citations.

5. (jamali2026thinkingmicroscopesagentic pages 3-4): Vida Jamali, Amirali Aghazadeh, and Joshua Kacher. Thinking microscopes: agentic ai and the future of electron microscopy. npj Computational Materials, Apr 2026. URL: https://doi.org/10.1038/s41524-026-02077-y, doi:10.1038/s41524-026-02077-y. This article has 1 citations and is from a peer-reviewed journal.

6. (jamali2026thinkingmicroscopesagentic pages 1-2): Vida Jamali, Amirali Aghazadeh, and Joshua Kacher. Thinking microscopes: agentic ai and the future of electron microscopy. npj Computational Materials, Apr 2026. URL: https://doi.org/10.1038/s41524-026-02077-y, doi:10.1038/s41524-026-02077-y. This article has 1 citations and is from a peer-reviewed journal.

7. (jamali2026thinkingmicroscopesagentic pages 2-3): Vida Jamali, Amirali Aghazadeh, and Joshua Kacher. Thinking microscopes: agentic ai and the future of electron microscopy. npj Computational Materials, Apr 2026. URL: https://doi.org/10.1038/s41524-026-02077-y, doi:10.1038/s41524-026-02077-y. This article has 1 citations and is from a peer-reviewed journal.

8. (niezgoda2013novelmicrostructurequantification pages 2-4): Stephen R Niezgoda, Anand K Kanjarla, and Surya R Kalidindi. Novel microstructure quantification framework for databasing, visualization, and analysis of microstructure data. Integrating Materials and Manufacturing Innovation, 2:54-80, Jul 2013. URL: https://doi.org/10.1186/2193-9772-2-3, doi:10.1186/2193-9772-2-3. This article has 162 citations and is from a peer-reviewed journal.

9. (niezgoda2013novelmicrostructurequantification pages 1-2): Stephen R Niezgoda, Anand K Kanjarla, and Surya R Kalidindi. Novel microstructure quantification framework for databasing, visualization, and analysis of microstructure data. Integrating Materials and Manufacturing Innovation, 2:54-80, Jul 2013. URL: https://doi.org/10.1186/2193-9772-2-3, doi:10.1186/2193-9772-2-3. This article has 162 citations and is from a peer-reviewed journal.

10. (feather2021anumericalstudy pages 2-3): William G. Feather, Hojun Lim, and Marko Knezevic. A numerical study into element type and mesh resolution for crystal plasticity finite element modeling of explicit grain structures. Computational Mechanics, 67:33-55, Sep 2021. URL: https://doi.org/10.1007/s00466-020-01918-x, doi:10.1007/s00466-020-01918-x. This article has 85 citations and is from a peer-reviewed journal.

11. (owens2025featureengineeringdescriptors pages 16-17): C. Braxton Owens, Nithin Mathew, Tyce W. Olaveson, Jacob P. Tavenner, Edward M. Kober, Garritt J. Tucker, Gus L. W. Hart, and Eric R. Homer. Feature engineering descriptors, transforms, and machine learning for grain boundaries and variable-sized atom clusters. npj Computational Materials, Jan 2025. URL: https://doi.org/10.1038/s41524-024-01509-x, doi:10.1038/s41524-024-01509-x. This article has 17 citations and is from a peer-reviewed journal.

12. (niezgoda2013novelmicrostructurequantification pages 22-23): Stephen R Niezgoda, Anand K Kanjarla, and Surya R Kalidindi. Novel microstructure quantification framework for databasing, visualization, and analysis of microstructure data. Integrating Materials and Manufacturing Innovation, 2:54-80, Jul 2013. URL: https://doi.org/10.1186/2193-9772-2-3, doi:10.1186/2193-9772-2-3. This article has 162 citations and is from a peer-reviewed journal.

13. (niezgoda2013novelmicrostructurequantification pages 7-9): Stephen R Niezgoda, Anand K Kanjarla, and Surya R Kalidindi. Novel microstructure quantification framework for databasing, visualization, and analysis of microstructure data. Integrating Materials and Manufacturing Innovation, 2:54-80, Jul 2013. URL: https://doi.org/10.1186/2193-9772-2-3, doi:10.1186/2193-9772-2-3. This article has 162 citations and is from a peer-reviewed journal.

14. (jamali2026thinkingmicroscopesagentic pages 4-5): Vida Jamali, Amirali Aghazadeh, and Joshua Kacher. Thinking microscopes: agentic ai and the future of electron microscopy. npj Computational Materials, Apr 2026. URL: https://doi.org/10.1038/s41524-026-02077-y, doi:10.1038/s41524-026-02077-y. This article has 1 citations and is from a peer-reviewed journal.

15. (niezgoda2013novelmicrostructurequantification pages 4-7): Stephen R Niezgoda, Anand K Kanjarla, and Surya R Kalidindi. Novel microstructure quantification framework for databasing, visualization, and analysis of microstructure data. Integrating Materials and Manufacturing Innovation, 2:54-80, Jul 2013. URL: https://doi.org/10.1186/2193-9772-2-3, doi:10.1186/2193-9772-2-3. This article has 162 citations and is from a peer-reviewed journal.

16. (niezgoda2013novelmicrostructurequantification pages 23-25): Stephen R Niezgoda, Anand K Kanjarla, and Surya R Kalidindi. Novel microstructure quantification framework for databasing, visualization, and analysis of microstructure data. Integrating Materials and Manufacturing Innovation, 2:54-80, Jul 2013. URL: https://doi.org/10.1186/2193-9772-2-3, doi:10.1186/2193-9772-2-3. This article has 162 citations and is from a peer-reviewed journal.

17. (jamali2026thinkingmicroscopesagentic pages 5-6): Vida Jamali, Amirali Aghazadeh, and Joshua Kacher. Thinking microscopes: agentic ai and the future of electron microscopy. npj Computational Materials, Apr 2026. URL: https://doi.org/10.1038/s41524-026-02077-y, doi:10.1038/s41524-026-02077-y. This article has 1 citations and is from a peer-reviewed journal.

18. (owens2025featureengineeringdescriptors pages 15-16): C. Braxton Owens, Nithin Mathew, Tyce W. Olaveson, Jacob P. Tavenner, Edward M. Kober, Garritt J. Tucker, Gus L. W. Hart, and Eric R. Homer. Feature engineering descriptors, transforms, and machine learning for grain boundaries and variable-sized atom clusters. npj Computational Materials, Jan 2025. URL: https://doi.org/10.1038/s41524-024-01509-x, doi:10.1038/s41524-024-01509-x. This article has 17 citations and is from a peer-reviewed journal.