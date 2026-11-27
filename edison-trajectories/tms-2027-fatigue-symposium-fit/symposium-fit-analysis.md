# TMS 2027 fit analysis — "Fatigue in Materials: Fundamentals, Multiscale Characterizations and Computational Modeling"

**ProgramMaster:** `B1D97A9DFD053F8985258D8700045BC7`
**Abstract deadline:** 2026-07-15
**Sponsors:** TMS MPMD + SMD; Additive Manufacturing, Advanced Characterization/Testing/Simulation, Computational Materials Science & Engineering, ICME, and Mechanical Behavior of Materials Committees.
**Edison persona mock review:** task `fc7c6405-877b-4794-9ab7-cae8eb9bd63d` (`LITERATURE_HIGH`) — result in [`edison-mock-review-result.md`](edison-mock-review-result.md).

## Scope (as published)
Characterizing and simulating **fatigue** damage; identifying microstructural weak links; enhancing fatigue strength/resistance — across metals, alloys, ceramics, composites, polymers. Topics:
1. Predictive fatigue methods (digital twins, data-driven, multiscale modeling)
2. Advanced experimental characterization (of fatigue)
3. Fatigue deformation processes
4. Extreme-environment fatigue
5. Non-metallic material fatigue
6. Industry-focused studies
7. **Additively manufactured material fatigue**

## Organizers & personas
| Organizer | Affiliation | Persona / relevance |
|---|---|---|
| **Krzysztof S. Stopka** | Purdue (ACME/Sangid) | Computational microstructure-sensitive fatigue; crystal plasticity; extreme-value stats of fatigue-indicator parameters; PRISMS-Fatigue; AM IN718; HEDM. |
| **Orion L. Kafka** | QuesTek (ex-NIST) | Data-driven/mechanistic HCF modeling; image-based multiscale models from measured microstructures; XCT of pores in AM metals; ICME + ML. |
| **Kelly E. Nygren** | Cornell / CHESS | Synchrotron ff-HEDM; in-situ fatigue loading; real-time big-data reduction; crack-initiation signatures in Ni superalloys. |
| **Pooriya D. Nezhadfar** | GE Aerospace | **AM (LB-PBF) aluminum fatigue — AlSi10Mg & Scalmalloy**; porosity/build-orientation/heat-treatment effects. Most materially on-topic for our alloy. |
| **Brandon T. Mackey** | Pratt & Whitney | Industry aerospace fatigue; component durability, metallurgy, reliability, qualification. |

## My honest read (before Edison firms it up): **a stretch — partial fit needing a real pivot**
- **The disqualifying gap:** this is a **fatigue** room, and the abstract does **no fatigue testing** — no S–N data, no crack-initiation study, no fatigue-life model. Its thesis is *compositional/microstructural measurement fidelity*, not damage mechanisms or life prediction.
- **Where it does touch the scope:**
  - Topic 7 (**AM material fatigue**): our alloy (AlSi10Mg) and the defect/porosity/phase metrology we optimize are exactly the *inputs* that govern AM-Al fatigue scatter — and Nezhadfar's own work is AlSi10Mg fatigue.
  - Topic 2 (**advanced experimental characterization**): EBSD/EDS acquisition optimization is characterization, but the room wants characterization *of fatigue damage*, not of as-built composition.
  - Topic 1 (**data-driven**): the provenance-tracked parameter dataset is a data-driven asset, but not aimed at fatigue prediction.
- **Committee tilt:** strongly **mechanics / life-prediction / defect-driven-fatigue** oriented (Stopka, Kafka, Nygren). A pure metrology/AI-tooling abstract with no fatigue outcome risks finding too few advocates — Nezhadfar is the likeliest ally.

## Tailoring playbook (if we pursue it)
The honest bridge is **"characterization-input fidelity as an upstream enabler of trustworthy microstructure-sensitive / defect-based fatigue prediction for AM aluminum"**:
- Show how EBSD indexing quality and EDS/composition error **propagate into** defect-population statistics, phase ID, and grain/texture descriptors that feed fatigue-indicator-parameter and defect-based fatigue models (Stopka/Kafka territory).
- Add (or promise) a concrete link from a parameter-fidelity knob → a fatigue-relevant microstructural input (pore/defect sizing, Si-network/eutectic morphology, GND/residual-stress proxies).
- Quantify "garbage-in" risk: mis-set EDS/EBSD → wrong defect/phase inputs → biased fatigue-life estimate.

## Edison verdict (landed) — **SUBMIT-IF-RETAILORED, confidence ~60%**
Panel of 5 organizer personas (full report: [`edison-mock-review-result.md`](edison-mock-review-result.md)). Votes: **3 Reject** (Stopka, Nygren, Mackey) / **2 Conditional-Accept** (Kafka, Nezhadfar). My pre-Edison read was confirmed: the disqualifier is **no fatigue outcome** — no S–N data, no crack-initiation, no fatigue-life model — so a fatigue audience asks "so what for fatigue life?" within 30 s and the abstract has no answer. **Single biggest risk:** reads as a metrology/AI talk that wandered into a fatigue session.

The door only opens with a real fatigue bridge — the panel's concrete asks:
- **Sensitivity study** (Stopka): feed the 40%-CI vs 77%-CI EBSD maps into a microstructure-sensitive analysis (even Schmid-factor) and show how the predicted fatigue-indicator-parameter / hotspot ranking changes. Grounded in Bandyopadhyay 2019 (10.1007/s11837-019-03551-3): ~20–25% variability in CP fatigue indicators from input uncertainty.
- **Downstream consumer** (Kafka): one worked example that consumes the provenance-tracked characterization output in a fatigue-prediction workflow.
- **Mechanical data** (Nezhadfar): even a small tensile/fatigue dataset on the same LPBF AlSi10Mg linking characterized microstructure to a mechanical outcome.
- **Qualification framing** (Mackey): path from reproducible settings → fatigue allowables / defect-acceptance criteria.

## Bottom line
**Weaker fit than the Fullwood MSD symposium** (Edison: ~60% vs ~High for Fullwood). Viable only if we add a fatigue-input-propagation angle; otherwise route to Fullwood MSD. Deadline Jul 15, 2026 (comfortable). Recommendation: **prefer the Fullwood MSD home venue** unless we specifically want a fatigue audience and are willing to add the sensitivity-study / mechanical-data bridge above.
