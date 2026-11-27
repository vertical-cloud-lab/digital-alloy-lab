# TMS 2027 Flyer 009 — symposium-fit analysis & persona-grounded mock review

Assessing whether the characterization-side TMS 2027 abstract (issue #102, PR #103) fits the symposium on
**[Flyer 009](https://www.tms.org/tms2027/downloads/flyers/TMS2027-CFA-Flyer-009.pdf)** — requested by
@sgbaird, who liked its sustainability focus and its explicit *"Advanced characterization of trace
elements"* topic. This file records (1) the flyer scope, (2) the organizer personas, (3) my own fit read,
and (4) the Edison `LITERATURE_HIGH` persona-mock-review prompt and its returned verdict.

---

## 1. The symposium (Flyer 009)

**Title:** *Characterizing Tramp Elements in Scrap Metals for Sustainable Manufacturing*
(Advanced Characterization Methods track).
**Sponsors:** TMS Extraction & Processing Division (division); TMS Materials Characterization Committee.

**Scope (verbatim gist):** the critical role of **tramp/residual elements** in **recycled and
scrap-based** metallic systems and their implications for **sustainable manufacturing**. As demand for
circular materials usage intensifies, increased reliance on scrap feedstocks introduces residuals such as
**Cu, Sn, Ni, Pb**, and others that are hard to remove during conventional processing — elements that
significantly influence phase stability, microstructural evolution, defect formation, and mechanical /
functional performance. The symposium spans ferrous, non-ferrous, and high-performance alloys and
integrates characterization, processing, and modeling toward robust manufacturing from recycled materials.

**Topics of interest:**
1. Advanced characterization of trace elements
2. Thermodynamic and kinetic modeling of impurity effects
3. Impacts on casting, forming, and additive manufacturing
4. Impurity mitigation, tolerance design, and alloy innovation
5. Industrial challenges and impacts on processing, microstructure, and performance

**Key dates (from flyer):** **Abstract Submissions Due — July 1, 2026**; Registration Opens Oct 2026;
Discount Registration Deadline Jan 31, 2027.

> ⚠️ **Deadline already past.** Today is 2026-07-07 — the July 1 abstract deadline is 6 days gone. Confirm
> late/rolling submission on [ProgramMaster](https://www.programmaster.org/TMS2027) before committing to
> this symposium. (Same caveat noted for Flyer 012.)

---

## 2. Organizing committee — personas (web research)

| Organizer | Affiliation | Research lens they'd review through |
| --- | --- | --- |
| **Eason (Yi-Sheng) Chen** | Nanyang Technological University | Advanced metallurgy; **cryo atom probe tomography (APT)** + EM of hydrogen/solute segregation at defects in steels — near-atomic-scale trace-element detection. Champions mechanistic, defect-resolved characterization; skeptical of bulk/empirical work without atomistic insight. |
| **Xin Wang** | Univ. of Alabama, Tuscaloosa | **In situ EM + nanomechanical testing**; processing–microstructure–property links for durable/sustainable structural materials. |
| **Ming Chen** | Univ. of Nevada, Reno | Processing/physical metallurgy; **metal AM (LPBF)**, **synchrotron XRD & tomography**, in situ mechanical testing. Champions synchrotron/in-situ methods and AM angles on residual-element effects. |
| **Yan Ma** | Delft Univ. of Technology | **"Sustainable Metallurgy" lab**: hydrogen-based direct reduction (green ironmaking) and **scrap-based steel design / residual-element tolerance** in a circular economy. **Most on-topic organizer.** |
| **Lawrence Cho** | Colorado School of Mines (ASPPRC; NIST-Boulder affiliate) | **Ferrous metallurgist**: AHSS, phase transformations, **Cu-induced hot shortness**, surface segregation, H/liquid-metal embrittlement. Values residuals-tied-to-embrittlement rigor. |
| **Leora Dresselhaus-Marais** | Stanford / SLAC / LLNL | **Dark-field X-ray microscopy (DFXM)** and synchrotron/XFEL **in-situ/operando imaging** of microstructure dynamics. Skeptical of static, ex-situ-only characterization. |
| **Mohsen Sanayei** | A. O. Smith | **Industry voice**: welding/brazing metallurgy, texture, corrosion, coatings, characterization. Values manufacturability / product-reliability relevance. |

**Committee synthesis:** strongly **steel / ferrous-metallurgy weighted** (Ma, Cho, E. Chen, Sanayei), with
sustainability framed through **scrap upcycling and residual-element tolerance** (Ma above all). It is
**characterization-depth-driven and biased toward advanced, in-situ / atomic-scale techniques** — APT,
synchrotron XRD/tomography, DFXM/XFEL, in-situ EM. Predominantly early-career academic with one clear
industry anchor (Sanayei). The least-represented interest — and the most likely to draw skepticism — is
**pure method/tooling work with weak metallurgical mechanism or weak scrap/recycling grounding.**

---

## 3. My fit read (before Edison)

**The good (real hooks):**
- Topic 1, *"Advanced characterization of trace elements,"* is a near-literal match to our EDS/XRF trace-Mg
  fidelity problem (Mg Kα / Al Kα overlap, standardless over-reporting).
- Topic 3, *"Impacts on... additive manufacturing,"* legitimizes the AM angle.
- The **sustainability / supply-chain-resilient** framing of FLAIME rhymes with the circular-materials
  mission.

**The mismatch (be honest):**
- **No scrap / recycling story.** The symposium is fundamentally about **secondary/scrap feedstocks** and
  residuals you can't remove. Our abstract is about *characterization-parameter optimization* on primary/
  virgin AlSi10Mg and lean designed alloys — not recycled Al, not tramp-element metallurgy.
- **Aluminum vs. a steel-leaning committee.** Cu/Sn/Ni/Pb tramp chemistry and hot-shortness are steel
  preoccupations; our Mg-in-Al problem is a *light-element analysis* problem, not a *residual-element
  tolerance* problem.
- **Method/AI-forward vs. mechanism-forward.** The committee rewards mechanistic, in-situ, atomic-scale
  characterization. Our contribution is a decision-support *system* + a parameter dataset — valuable, but
  orthogonal to what excites APT/synchrotron/DFXM reviewers.
- **Ex-situ vs. in-situ bias.** Several organizers (M. Chen, Dresselhaus-Marais) live in operando imaging;
  our SEM/EDS/EBSD/XRD/XRF setup is static ex-situ.

**Preliminary verdict:** a **partial fit that needs a genuine pivot** to belong — not a drop-in. The
honest bridge is to reframe around **trace/residual-element quantification *fidelity* in secondary/recycled
aluminum**: the metrology problem of *certifying scrap-derived Al feedstock composition* (Cu, Sn, Ni, Pb,
Fe, Zn) with EDS/XRF/ICP, and how parameter optimization de-risks residual-element measurement for
circular AM. Whether that pivot is worth it — vs. keeping the abstract in its native "Rapid Acquisition /
Large Datasets" symposium — is exactly what the Edison persona panel was asked to adjudicate (below).

---

## 4. Edison `LITERATURE_HIGH` persona mock review

**Job:** `JobNames.LITERATURE_HIGH`, task `78ab69c6-098c-4686-8638-c44ba4018dbb`, submitted 2026-07-07 via
`EdisonClient` (`api.platform.edisonscientific.com`). The full prompt (panel of all 7 organizers; sections
A–E: fit assessment, per-organizer mock review, verdict, tailoring playbook, literature) is reproduced in
[`edison-prompt.md`](edison-prompt.md).

The returned report is saved in [`edison-mock-review.md`](edison-mock-review.md) with references in
[`edison-references.md`](edison-references.md).
