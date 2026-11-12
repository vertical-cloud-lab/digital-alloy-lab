# AM Aluminum Alloys in Downstream Applications

This document compiles Edison Scientific LITERATURE search results on which additively manufactured aluminum alloys have reached real-world downstream applications, what properties enabled their adoption, and what qualification pathways were used.

## Edison Task IDs

| Query | Task ID |
|---|---|
| Downstream applications | `652fa29c-67f8-4c02-beda-3e632f700162` |
| Qualification standards | `251b0653-1449-4894-aa21-132f2441ac78` |

---

## Query 1: Downstream Applications

Question: What additively manufactured aluminum alloys have been adopted in real-world downstream applications (aerospace, automotive, defense, space, consumer products)? For each alloy system, identify the specific application, the AM process used (LPBF, DED, WAAM, EBM), the component or product, the end user or OEM, and the key material properties (strength, fatigue, thermal stability, corrosion resistance, weight savings) that qualified the alloy for that application. Include AlSi10Mg, Scalmalloy, A20X, Al-Cu-Mg-Ag, and any other AM Al alloys with documented industrial deployment.

## Summary of documented downstream adoption of AM aluminum alloys

The strongest downstream (real-world) adoption evidence in the retrieved corpus is concentrated in LPBF/LBM aluminum-silicon alloys (AlSi10Mg, AlSi7Mg, AlSi40) and Scalmalloy (Al–Mg–Sc–Zr), mainly for space/aerospace structures and RF hardware, plus automotive racing hardware and a full-size LPBF aluminum aircraft engine demonstrator. By contrast, for A20X/A205 (Al–Cu–Mg–Ag–TiB2) and related Al–Cu–Mg–Ag systems, the retrieved sources document extensive LPBF processability and mechanical/fatigue qualification work but do not provide a clearly attributed deployed component with a named OEM/end user; these alloys are therefore reported here as **qualification-stage within this evidence set** rather than confirmed industrial deployment. (wang2024areviewon pages 15-18, avateffazeli2022microstructuremechanicaland pages 1-5)

## Evidence-backed deployments by alloy system

### AlSi10Mg (Al–Si–Mg)

* **Space: satellite structures** — Bright Laser Technologies reports LPBF manufacture of **satellite deployer main frames and cabin doors** in **AlSi10Mg** for the **“Dalian No. 1–Lianli” satellite**, giving component scale and thin-wall capability (frame ~400×400×500 mm; ~1 mm minimum wall). (wang2024areviewon pages 15-18)
* **Aerospace: aircraft bracket** — A topology-optimized aircraft bracket was produced by **laser beam melting (LBM/SLM)** using **AlSi10Mg** on an **SLM 250 HL** platform, achieving about **60% weight reduction** versus the baseline and requiring heat treatment plus machining of functional surfaces as part of qualification/finishing. (klippstein2019developmentproductionand pages 1-3)
* **Aerospace propulsion: injector** — A **mass-optimized cryogenic propellant injector** is shown as being fabricated in **AlSi10Mg by L‑PBF** as an application example in NASA-oriented process selection work. (gradl2022robustmetaladditive pages 5-7)
* **Qualification-relevant properties** — Reported LPBF AlSi10Mg property envelope used for applicability discussions includes **~98–99% density**, **~350–400 MPa tensile strength**, and **~8–12% ductility** (as-built ranges as summarized in a review). (dasari2026reviewofadditive pages 5-7)

### Scalmalloy® (Al–Mg–Sc–Zr)

* **Space (telecom satellites): in-orbit heritage and scale-up** — A CNES/Thales Alenia Space/LISI Aerospace AM program describes developing/qualifying Scalmalloy® for satellite parts via **laser beam melting (LBM)** and states that **“more than 100 metallic LBM parts are currently in-orbit on Thales Alenia Space telecom satellites”** (in aluminum LBM secondary structures), while targeting new thermal and RF applications; Scalmalloy typical properties are given around **UTS ~515 MPa**, density ~2.7 kg/dm³, elongation ~7% (datasheet values cited). (france2019additivemanufacturingof pages 1-3)
* **Space (mission hardware): inspected/qualified parts** — Space hardware examples manufactured in **Scalmalloy® by LPBF** and inspected by X‑ray CT include a **monitoring camera bracket for JUICE** and **fairings for the Clean Sky 2 air demonstrator** (voxel size 98 µm for CT in these cases), illustrating the inspection/qualification pathway used for critical aerospace/space parts. (galleguillos2023ndtforqualification pages 1-4)
* **Space RF hardware: feed chains/waveguides** — RF components manufactured in **Scalmalloy** using **additive layer manufacturing (ALM) on an EOS400-class powder-bed system** include a **2.53 m meander waveguide** and a **Ku-band orthomode transducer (OMT)** with a directly printed horn option; motivations include Scalmalloy’s **higher mechanical strength than AlSi10Mg** and “good electrical properties,” with reported lower manufacturing costs and reduced integration effort via printed integration, while noting RF-loss tradeoffs versus conventional manufacturing. (kilian2017rffeedchain pages 2-4)
* **Nanosatellite optical payload structures** — A flight-qualification-oriented nanosatellite study used Scalmalloy for an **optical bench/MWIR camera platform (including lens mounting, radiator, baffle)**, motivated by **high strength-to-weight** and **low CTE** to protect alignment and reduce thermal stresses; the part is intended to withstand launch vibration plus on-orbit thermal environments. (bierdel2018towardsflightqualification pages 2-4)
* **Qualification-relevant properties** — Additional Scalmalloy development data include: low porosity verified by CT, heat-treatment windows (e.g., 325–350 °C aging) and tensile levels around UTS ~514–515 MPa, YS ~496–508 MPa with ~5% elongation in one industrial development report, supporting strength-based selection for satellite structures. (france2019additivemanufacturingof pages 3-7)

### AlSi7Mg (Al–Si–Mg)

* **Space: satellite antenna bracket** — Thales Alenia Space and Poly‑Shape produced **LPBF AlSi7Mg antenna brackets** for **Koreasat‑5A/7**, consolidating **nine parts into one** and reporting **~22% weight reduction** and **~30% cost reduction** (final bracket mass 1.13 kg). (wang2024areviewon pages 15-18)

### AL250C (AM-specific Al alloy)

* **Aerospace propulsion: engine demonstrator** — AmPro‑Innovations manufactured a **full-size LPBF aircraft engine** using **AL250C**, reporting high strength (**YS ~580 MPa, UTS >590 MPa, elongation ~11%**) and elevated-temperature durability (**>5000 h at 250 °C**), with development-cycle and delivery-time reductions. (wang2024areviewon pages 15-18)

### AlSi40 (hyper-eutectic Al–Si, high-Si)

* **Space optics/astronomy: LPBF/SLM mirror demonstrators and TRL progression** — Multiple ESA-linked programs report **LPBF/SLM AlSi40 mirrors** with **electroless NiP coating** for space optics to address CTE matching and enable lightweight lattice/monolithic designs.
  * A feasibility/demonstrator activity (SME4ALM initiative under DLR/ESA; KTO + Fraunhofer IWS) selected **SLM AlSi40 + NiP** to achieve CTE compatibility for cryogenic mirrors and pursued optical/mechanical targets (e.g., WFE targets, eigenfrequency targets) as part of TRL maturation rather than completed flight deployment. (eberle2019additivemanufacturingof pages 1-4)
  * The PAM project (KTO + Fraunhofer IWS + Airbus Defence & Space + ESA/ESTEC) reports **reliable LPBF printing of AlSi40**, improvements in stiffness/SFE metrics (up to ~40% reported), and explicit **TRL 4 achieved** with **TRL ≥5 targeted** via space-representative thermal-vacuum and mechanical testing. (reutlinger2023printedathermalmirror pages 4-6, reutlinger2023printedathermalmirror pages 1-4)
  * A Fraunhofer IOF / university study reports an SLM AlSi40 mirror with **~60.5% mass reduction**, **porosity <0.05%**, and post-processed optical quality (form deviation <80 nm p‑v; roughness ~1 nm rms), showing the property basis for adoption in spaceborne mirrors. (hilpert2019designadditivemanufacturing pages 1-3)

## A20X / A205 and other Al–Cu–Mg–Ag systems (qualification evidence, but no named deployed component in this corpus)

A205/A20X (Al–Cu–Mg–Ag–TiB2) is repeatedly described as a high-strength, aerospace-/automotive-relevant AM alloy family and is processed by **LPBF on EOS M290** with fatigue testing and heat-treatment development, supporting its qualification potential. However, in the retrieved texts it is not tied to a specific deployed downstream part with a named OEM/end user, so it cannot be asserted here as adopted in downstream industrial products based on this evidence set. (avateffazeli2022microstructuremechanicaland pages 1-5, gradl2022robustmetaladditive pages 5-7)

## Consolidated evidence table

| Alloy system | Sector/application | Component/product | End user/OEM (and key partners/manufacturer if stated) | AM process | Qualification/benefit notes |
|---|---|---|---|---|---|
| AlSi10Mg | Space | Satellite deployer main frame and cabin doors for Dalian No. 1–Lianli satellite | Bright Laser Technologies; Dalian No. 1–Lianli satellite program | LPBF | Large thin-wall space structures; main frame ~400×400×500 mm, min wall ~1 mm; demonstrates real satellite deployment of LPBF AlSi10Mg hardware (wang2024areviewon pages 15-18) |
| AlSi10Mg | Aerospace | Topology-optimized aircraft bracket | Aircraft bracket case study; built on SLM 250 HL | LBM / SLM | ~60% weight reduction; more homogeneous stress distribution; post-build heat treatment, smoothing, and machining required; positioned for aviation qualification (klippstein2019developmentproductionand pages 1-3) |
| AlSi10Mg | Aerospace / propulsion | Mass-optimized cryogenic propellant injector | NASA/aerospace example in AM process-selection review | L-PBF | Real aerospace component example; selected for mass optimization and internal-feature capability; review notes AlSi10Mg maturity across PBF/DED process families (gradl2022robustmetaladditive pages 5-7) |
| AlSi10Mg | General qualification context | LPBF AlSi10Mg production baseline | Multiple industrial users | LPBF | Typical qualification envelope reported at 98–99% density, ~350–400 MPa tensile strength, ~8–12% ductility; supports use where lightweight, near-full-density parts are needed (dasari2026reviewofadditive pages 5-7) |
| Scalmalloy (Al-Mg-Sc-Zr) | Space / telecom satellites | Satellite secondary structures and Scalmalloy space demonstrator; includes antenna/TMTC/Ku support classes | Thales Alenia Space; CNES; LISI Aerospace AM; alloy from APWORKS/Airbus Group | LBM / LPBF | >100 metallic LBM parts already in orbit on Thales Alenia Space telecom satellites; Scalmalloy pursued for higher strength than conventional Al-Si, good corrosion resistance and weldability, possible Ti replacement where strength + thermal conductivity matter; typical post-HT properties ~UTS 515 MPa, elongation ~7% (france2019additivemanufacturingof pages 1-3, france2019additivemanufacturingof pages 3-7) |
| Scalmalloy (Al-Mg-Sc-Zr) | Space / qualification | Monitoring camera bracket for JUICE; fairings for Clean Sky 2 demonstrator | CATEC; JUICE mission; Clean Sky 2 air demonstrator | LPBF | CT-based NDT highlighted for qualification; voxel size 98 µm for these Scalmalloy parts; example of flight-hardware inspection workflow under ECSS/airframer defect criteria (galleguillos2023ndtforqualification pages 1-4) |
| Scalmalloy (Al-Mg-Sc-Zr) | Space RF hardware | 2.53 m meander waveguide; Ku-band orthomode transducer with directly printed horn | ESA/ESTEC-supported work; Airbus/APWORKS lineage for alloy | ALM / PBF on EOS400-class machine | Chosen for good electrical properties and markedly higher mechanical strength than AlSi10Mg; lower manufacturing cost and reduced integration effort via part consolidation, though RF losses remained higher than conventionally machined parts (kilian2017rffeedchain pages 2-4) |
| Scalmalloy (Al-Mg-Sc-Zr) | Space / nanosatellite optics | Optical bench, MWIR camera platform, lens mount, radiator, baffle | Nanosatellite optical payload demonstrator | LPBF / SLM | Selected for high strength-to-weight ratio and low CTE to preserve camera-lens alignment and manage thermal stress/vibration; demonstrates downstream satellite subsystem development (bierdel2018towardsflightqualification pages 2-4) |
| AlSi7Mg | Space / telecom satellites | Antenna bracket for Koreasat-5A/7 | Thales Alenia Space with Poly-Shape | LPBF | Nine parts consolidated into one; final bracket mass 1.13 kg; ~22% weight reduction and ~30% cost reduction (wang2024areviewon pages 15-18) |
| AL250C | Aerospace / engine | Full-size aircraft engine | AmPro-Innovations | LPBF | AM-specific high-temperature Al alloy; reported YS ~580 MPa, UTS >590 MPa, elongation ~11%, service life >5000 h at 250°C; development cycle reduced ~75%, delivery time reduced ~50% (wang2024areviewon pages 15-18) |
| AlSi40 | Space optics / astronomy | Printed athermal mirror / PAM demonstrator; scanning mirror and representative mirror structures | Kampf Telescope Optics, Fraunhofer IWS, Airbus Defence & Space, ESA/ESTEC, DLR/ESA SME4ALM / ESA GSTP | SLM / LPBF | Chosen for CTE compatibility with NiP coating and high specific stiffness; reported ~30–40% improvement in stiffness/SFE metrics in project context, TRL 4 achieved and TRL ≥5 targeted; cryogenic/space mirror demonstrators use lattice/hollow structures (eberle2019additivemanufacturingof pages 1-4, reutlinger2023printedathermalmirror pages 4-6, reutlinger2023printedathermalmirror pages 1-4, eberle2019additivemanufacturingof pages 12-12) |
| AlSi40 | Space optics | Hyper-eutectic AlSi40 mirror demonstrator | Fraunhofer IOF / Friedrich Schiller University Jena | SLM | ~60.5% mass reduction, porosity <0.05%, final form deviation <80 nm p-v, roughness ~1 nm rms after NiP + ultra-precision finishing; demonstrates why AlSi40 is compelling for lightweight mirrors needing thermal match to NiP (hilpert2019designadditivemanufacturing pages 1-3) |
| A20X / A205 (Al-Cu-Mg-Ag-TiB2) | Aerospace / automotive relevance claimed, but no explicit downstream deployment found in retrieved texts | No named deployed component/OEM identified in retrieved evidence | Processed and characterized by multiple research/qualification groups | LPBF | Retrieved texts show AM process maturity claims, aerospace-approved family language, and mechanical/fatigue/heat-treatment studies, but did not document a specific in-service product, OEM, or flight/vehicle deployment; treat as qualification-stage evidence rather than confirmed downstream adoption in this evidence set (avateffazeli2022microstructuremechanicaland pages 1-5, gradl2022robustmetaladditive pages 5-7, montanari2023additivemanufacturingof pages 14-16) |


*Table: This table compacts the retrieved evidence into alloy-by-alloy downstream application rows, listing the component, OEM/end user, AM process, and the key material or qualification factors that enabled use. It also flags where the evidence supports only qualification-stage status rather than a clearly documented deployed product.*

## Notes on process coverage and evidence gaps

* In this evidence set, essentially all aluminum-alloy downstream adoptions are tied to **powder-bed laser processes** (LPBF/LBM/SLM/ALM). Evidence for **wire-DED/WAAM/EBM** aluminum-alloy deployments in downstream industrial products was not found among the retrieved sources, so they are not included as confirmed deployments here. (montanari2023additivemanufacturingof pages 14-16, dasari2026reviewofadditive pages 5-7)
* Aerospace/space qualification drivers repeatedly emphasized include **mass reduction**, **high specific strength**, **fatigue considerations and surface condition**, **CTE/thermal stability for optical payloads**, and **NDT/CT defect-threshold compliance** for critical hardware. (wang2024areviewon pages 15-18, kilian2017rffeedchain pages 2-4, galleguillos2023ndtforqualification pages 1-4, eberle2019additivemanufacturingof pages 1-4)


References

1. (wang2024areviewon pages 15-18): Xin Wang, Dongyun Zhang, Ang Li, Denghao Yi, and Tianci Li. A review on traditional processes and laser powder bed fusion of aluminum alloy microstructures, mechanical properties, costs, and applications. Materials, 17:2553, May 2024. URL: https://doi.org/10.3390/ma17112553, doi:10.3390/ma17112553. This article has 39 citations.

2. (avateffazeli2022microstructuremechanicaland pages 1-5): Maryam Avateffazeli, Md Faysal Khan, Nima Shamsaei, and Meysam Haghshenas. Microstructure, mechanical, and fatigue properties of a laser powder bed fused al-cu-mg-ag-ti-b (a205) alloy. Unknown, Jan 2022. URL: https://doi.org/10.26153/tsw/44159, doi:10.26153/tsw/44159. This article has 3 citations.

3. (klippstein2019developmentproductionand pages 1-3): Helge Klippstein, Anne Duchting, Thomas Reiher, Florian Hengsbach, Dennis Menge, and Hans-Joachim Schmid. Development, production and post-processing of a topology optimized aircraft bracket. Unknown, Jan 2019. URL: https://doi.org/10.26153/tsw/17448, doi:10.26153/tsw/17448. This article has 9 citations.

4. (gradl2022robustmetaladditive pages 5-7): P. Gradl, Darren C. Tinker, A. Park, O. Mireles, Marissa B. Garcia, Ryan P. Wilkerson, and Christopher Mckinney. Robust metal additive manufacturing process selection and development for aerospace components. Journal of Materials Engineering and Performance, 31:6013-6044, Apr 2022. URL: https://doi.org/10.1007/s11665-022-06850-0, doi:10.1007/s11665-022-06850-0. This article has 285 citations and is from a peer-reviewed journal.

5. (dasari2026reviewofadditive pages 5-7): Jayaram Dasari and M. Anthony Xavior. Review of additive manufacturing and post processing techniques for aluminium alloys with focus on microstructure changes mechanical performance and emerging trends. Discover Mechanical Engineering, Apr 2026. URL: https://doi.org/10.1007/s44245-026-00189-9, doi:10.1007/s44245-026-00189-9. This article has 0 citations and is from a peer-reviewed journal.

6. (france2019additivemanufacturingof pages 1-3): TAS FRANCE. Additive manufacturing of scalmalloy® satellite parts. Unknown journal, 2019.

7. (galleguillos2023ndtforqualification pages 1-4): Carlos Galleguillos, Antonio Periñán, Sergio González, and Fernando Lasagni. Ndt for qualification of space hardware made by additive manufacturing. Research and Review Journal of Nondestructive Testing, Aug 2023. URL: https://doi.org/10.58286/28124, doi:10.58286/28124. This article has 1 citations.

8. (kilian2017rffeedchain pages 2-4): Michael Kilian, Christian Hartwanger, and Michael Schneider. Rf feed chain components manufactured by additive manufacturing techniques. 2017 International Conference on Electromagnetics in Advanced Applications (ICEAA), pages 555-558, Sep 2017. URL: https://doi.org/10.1109/iceaa.2017.8065305, doi:10.1109/iceaa.2017.8065305. This article has 3 citations.

9. (bierdel2018towardsflightqualification pages 2-4): Marius Bierdel, Klaus Hoschke, Aron Pfaff, Martin Schimmerohn, and Frank Schäfer. Towards flight qualification of an additively manufactured nanosatellite component. Text, 2018. URL: https://doi.org/10.24406/publica-fhg-404002, doi:10.24406/publica-fhg-404002. This article has 2 citations and is from a peer-reviewed journal.

10. (france2019additivemanufacturingof pages 3-7): TAS FRANCE. Additive manufacturing of scalmalloy® satellite parts. Unknown journal, 2019.

11. (eberle2019additivemanufacturingof pages 1-4): Sebastian Eberle, Arnd Reutlinger, Bailey Curzadd, Michael Mueller, Mirko Riede, Christoph Wilsnack, Ana Brandão, Laurent Pambaguian, André Seidel, Elena López, Frank Brueckner, Eckhard Beyer, and Christoph Leyens. Additive manufacturing of an alsi40 mirror coated with electroless nickel for cryogenic space applications. International Conference on Space Optics — ICSO 2018, 11180:1118015-1118015-12, Jul 2019. URL: https://doi.org/10.1117/12.2535960, doi:10.1117/12.2535960. This article has 20 citations.

12. (reutlinger2023printedathermalmirror pages 4-6): Arnd Reutlinger, Sebastian Eberle, Christoph Wilsnack, Juliane Moritz, Andreas Stute, Stefano Lucarelli, Ana Brandão, and Joel Larsson. Printed athermal mirror (pam) based on alsi40 and nip coating for space application. International Conference on Space Optics — ICSO 2022, 12777:127772X-127772X-18, Jul 2023. URL: https://doi.org/10.1117/12.2690312, doi:10.1117/12.2690312. This article has 2 citations.

13. (reutlinger2023printedathermalmirror pages 1-4): Arnd Reutlinger, Sebastian Eberle, Christoph Wilsnack, Juliane Moritz, Andreas Stute, Stefano Lucarelli, Ana Brandão, and Joel Larsson. Printed athermal mirror (pam) based on alsi40 and nip coating for space application. International Conference on Space Optics — ICSO 2022, 12777:127772X-127772X-18, Jul 2023. URL: https://doi.org/10.1117/12.2690312, doi:10.1117/12.2690312. This article has 2 citations.

14. (hilpert2019designadditivemanufacturing pages 1-3): Enrico Hilpert, Johannes Hartung, Henrik von Lukowicz, Tobias Herffurth, and Nils Heidler. Design, additive manufacturing, processing, and characterization of metal mirror made of aluminum silicon alloy for space applications. Optical Engineering, 58:092613-092613, May 2019. URL: https://doi.org/10.1117/1.oe.58.9.092613, doi:10.1117/1.oe.58.9.092613. This article has 84 citations and is from a peer-reviewed journal.

15. (eberle2019additivemanufacturingof pages 12-12): Sebastian Eberle, Arnd Reutlinger, Bailey Curzadd, Michael Mueller, Mirko Riede, Christoph Wilsnack, Ana Brandão, Laurent Pambaguian, André Seidel, Elena López, Frank Brueckner, Eckhard Beyer, and Christoph Leyens. Additive manufacturing of an alsi40 mirror coated with electroless nickel for cryogenic space applications. International Conference on Space Optics — ICSO 2018, 11180:1118015-1118015-12, Jul 2019. URL: https://doi.org/10.1117/12.2535960, doi:10.1117/12.2535960. This article has 20 citations.

16. (montanari2023additivemanufacturingof pages 14-16): Roberto Montanari, Alessandra Palombi, Maria Richetta, and Alessandra Varone. Additive manufacturing of aluminum alloys for aeronautic applications: advantages and problems. Metals, 13:716, Apr 2023. URL: https://doi.org/10.3390/met13040716, doi:10.3390/met13040716. This article has 66 citations.

---

## Query 2: Qualification Standards and Certification Pathways

Question: What qualification standards, certification pathways, and property requirements have enabled AM aluminum alloys to transition from R&D to production use? Cover aerospace (NASA, ESA, Airbus, Boeing), automotive (Formula 1, OEMs), and defense applications. For each case, specify the alloy, the mechanical property thresholds that had to be met (yield strength, ultimate tensile strength, elongation, fatigue limit), the testing and qualification process, and whether the component replaced a traditionally manufactured part. Include specific examples of flight-qualified or production-qualified AM Al components.

## Scope and evidentiary limits
This response summarizes qualification standards, certification pathways, and documented property/inspection requirements that have enabled additively manufactured (AM) aluminum-family alloys (AlSi10Mg, Scalmalloy®, and a novel Al-HS1) to move from R&D into (i) flight hardware used in space/aerospace programs and (ii) limited automotive/defense contexts.

The retrieved full-text corpus contains strong evidence for NASA and ESA/ECSS qualification frameworks and for specific flight-hardware examples (PROBA-3 AlSi10Mg antenna; JUICE Scalmalloy bracket; Clean Sky 2 Scalmalloy fairings) with explicit NDT acceptance criteria, but it does **not** contain Airbus/Boeing internal minimum tensile/fatigue allowables for specific production parts nor a Boeing-specific aluminum part qualification dossier. Automotive Formula 1 and OEM production cases are only weakly documented in the accessible sources (mostly narrative mentions) and therefore cannot be fully populated with property thresholds and test matrices.

## Cross-cutting mechanisms that enabled transition to production use
### 1) Qualification is process-centric: MPS/QMP/PPP, witness coupons, and class-based tailoring (NASA)
NASA’s approach (originating from Marshall Space Flight Center) formalizes AM into configuration-controlled packages that make properties reproducible and auditable rather than “one-off” R&D results:

* **Materials Property Suite (MPS)**: a collection of statistically significant material properties (intended to be MMPDS-equivalent) for a specific AM alloy/condition, applicable only when built under a qualified part process with first-article inspection and continuous monitoring. (russell2019nasa’splansfor pages 2-5)
* **Qualified Metallurgical Process (QMP)**: alloy- and machine-specific, analogous to a weld procedure qualification record; includes powder feedstock controls and recycle limits, a fusion process specification, microstructural and thermal processing evaluation, and mechanical-property baseline generation. (russell2019nasa’splansfor pages 2-5)
* **Witness specimens** (metallurgical, tensile for strength/ductility, and fatigue) with prescribed types/quantities/layout/test methods and acceptance criteria to demonstrate “systemic process health.” (russell2019nasa’splansfor pages 2-5)
* **Part Production Plan (PPP)**: configuration-controlled documentation of AM-unique process controls not captured on drawings. (russell2019nasa’splansfor pages 2-5)
* **Class-based tailoring**: requirements matrices (as-written/optional/tailorable) driven by part class (A/B/C) and risk gates; Class A includes fracture-critical per NASA-STD-5019A and other high-consequence failures. (russell2019nasa’splansfor pages 2-5)

NASA also shows explicit, property-linked acceptance/margin logic for fatigue/fracture assessments, e.g.:
* local plastic strain < 0.005;
* high-cycle fatigue (HCF) improved surfaces: additional life factor or **20% below required fatigue limit cyclic stress range**;
* HCF as-built surfaces: additional life factor or **40% below required fatigue limit cyclic stress range**. (russell2019nasa’splansfor pages 2-5)

These requirements are not alloy-specific allowables; rather, they define **how** allowables and structural margins are established and controlled for AM parts.

### 2) Defect-based property protection: CT as a mandatory gate for critical spaceflight aluminum hardware (ESA/ECSS + OEM specs)
For LPBF flight hardware, quality assurance has shifted strongly toward “defect state control” as a proxy for fatigue/durability, because internal flaws dominate fatigue initiation.

* **ECSS-Q-ST-70-80C** (ESA-coordinated) is cited as indicating **CT inspections shall be carried out especially for critical structural and functional components**. (galleguillos2023ndtforqualification pages 1-4)
* Airbus’ AM technical specification **AIMS03-22-000** is cited with explicit **defect-size acceptance examples** used during qualification:
  * **200 µm** maximum allowable defect for structural critical parts or non-critical parts with fatigue load requirements
  * **500 µm** for non-structural or structural parts without fatigue requirements. (galleguillos2023ndtforqualification pages 1-4)
* CT practice is tied to standards for operation/interpretation (ASTM E1570-19; ISO 15708-3) and uses **IQIs** (calibrated internal holes 100–1000 µm) and detectability rules (e.g., ≥3 voxels in a row or 33 voxels in volume) to ensure the inspection sensitivity matches the acceptance criterion. (galleguillos2023ndtforqualification pages 1-4)

This pathway makes the transition to production feasible by replacing “hero-part” qualification with repeatable inspection sensitivity and defect acceptance classes.

## Aerospace: documented flight/production-qualified AM aluminum(-family) cases
### ESA/ECSS flight hardware qualified by CT/NDT: PROBA-3 AlSi10Mg antenna
A concrete example of flight hardware is a **helix antenna for the PROBA-3 satellite**, made by LPBF in **AlSi10Mg** and inspected by micro-CT at CATEC. (galleguillos2023ndtforqualification pages 1-4, galleguillos2023ndtforqualification media 19ce40e6)

**Qualification/inspection process and requirements**
* ECSS-Q-ST-70-80C cited as requiring CT for critical components. (galleguillos2023ndtforqualification pages 1-4)
* CT performed per ASTM E1570-19 and ISO 15708-3. (galleguillos2023ndtforqualification pages 1-4)
* Acceptance logic uses Airbus AIMS03-22-000 defect-size examples (200/500 µm). (galleguillos2023ndtforqualification pages 1-4)
* For PROBA-3 antenna, the inspection voxel size was adjusted to **64 µm**, consistent with detecting ~200 µm-class defects using voxel-count rules. (galleguillos2023ndtforqualification pages 1-4)

**Mechanical property thresholds**
The qualification document is inspection-centric and does not publish tensile/fatigue acceptance numbers for the antenna itself. (galleguillos2023ndtforqualification pages 1-4)

To contextualize why defect control is central, representative AlSi10Mg fatigue strengths from dedicated fatigue studies include ~**92 ± 15 MPa (T5)** and **108 ± 5 MPa (rapid T6)** at room temperature (reported as σfs,50%). (egidio2023roomandhightemperature pages 7-9)

**Replacement status**
Whether this antenna replaced a traditionally manufactured antenna is not specified in the source. (galleguillos2023ndtforqualification pages 1-4)

### ESA/ECSS flight hardware: JUICE monitoring camera bracket in Scalmalloy®
The same CT-based qualification paper documents a **JUICE monitoring camera bracket (JMC)** produced by LPBF in **Scalmalloy®** as a flight component. (galleguillos2023ndtforqualification pages 1-4, galleguillos2023ndtforqualification media 19ce40e6)

**Material capability thresholds (coupon-level material context)**
A separate Scalmalloy-focused study reports Scalmalloy yield strength **~450 MPa** and elongation **>10%**, with properties comparable to legacy aerospace high-strength Al alloys (AA7075-T7351, AA7050-T7451). (jones2021characterisingcrackgrowth pages 1-3)

**Qualification/inspection pathway**
The flight-hardware CT pathway is as above (ECSS-Q-ST-70-80C CT expectation; ASTM E1570/ISO 15708-3; IQIs; acceptance based on end-user safety class). (galleguillos2023ndtforqualification pages 1-4)

**Replacement status**
Not stated. (galleguillos2023ndtforqualification pages 1-4)

### Clean Sky 2 aeronautic demonstrator: Scalmalloy® fairings
The same NDT/qualification work lists **aluminium fairings for the Clean Sky 2 IADP demonstrator**, manufactured in **Scalmalloy®** and inspected with the same CT qualification workflow. (galleguillos2023ndtforqualification pages 1-4, galleguillos2023ndtforqualification media 19ce40e6)

**Mechanical thresholds and replacement status**
Not published for the fairings in the retrieved text; the evidence primarily supports the NDT-based qualification and acceptance pathway (including 200/500 µm defect classes). (galleguillos2023ndtforqualification pages 1-4)

### Production-qualification style example: AM hydraulic manifold in novel Al-HS1
A documented “transition to industrial standards and airworthiness requirements” case is an LPBF hydraulic manifold made in **forAM® Al-HS1** (Al–Mn–Cr–Zr based) with an explicit qualification test matrix. (arena2024novelaluminumalloy pages 11-14)

**Alloy and process**
* EOS M290 LPBF; relative density reported >99.7%. (arena2024novelaluminumalloy pages 4-6)

**Mechanical property thresholds/values**
* Yield strength reported to increase from **~250 MPa (as-printed)** to **~350 MPa (heat treated at 375 °C)**. (arena2024novelaluminumalloy pages 4-6)
* Fatigue testing was performed by fully reversed four-point bending (R = −1), staircase method, with **run-out at 2×10^6 cycles**. (arena2024novelaluminumalloy pages 4-6)

**Qualification/acceptance testing**
* Proof pressure: **1.5× DOP** held 2 min (twice)
* Burst pressure: **2.5× DOP** (destructive, performed last)
* Endurance/cycling: **5,000 cycles** used as functional window for an emergency control module; SAE ARP1383 referenced for 100,000-cycle utility valve testing
* Test environment: MIL-PRF-5606J hydraulic fluid; NAS 1638 contamination class 7 or better
* NDI: dye-penetrant immersion and UV inspection. (arena2024novelaluminumalloy pages 11-14)

**Replacement status**
Not explicitly stated in the retrieved pages. (arena2024novelaluminumalloy pages 11-14)

## Automotive (Formula 1, OEMs): evidence found vs. missing
### Racing-car structural component: AlSi10Mg SLM clutch lever (validated replacement)
A documented racing-car component redesign shows how automotive validation can be property-threshold-driven even without a formal aerospace-style certification framework.

* **Component**: clutch lever
* **Process / alloy**: SLM of **AlSi10Mg**
* **Threshold used**: maximum stress must remain below the **yield limit ~220 MPa**; maintained safety factor >3.0
* **Qualification/validation**: FEM before/after topology optimization and experimental testing; the redesigned lever replaced the previous part in the vehicle system. (mikulikova2023topologyoptimizationof pages 1-2)

Fatigue limits, UTS, and elongation acceptance values were not reported for this part. (mikulikova2023topologyoptimizationof pages 1-2)

### Formula 1 piston mention (insufficient qualification detail)
A narrative review states that **AlSi10Mg** has been used by **Mahle Powertrain** to produce pistons for Formula 1. (arena2024novelaluminumalloy pages 4-6)

However, the retrieved evidence does not include the required details (property thresholds, fatigue limits, test/qualification route, and replacement confirmation) to treat this as a fully documented production qualification case. (arena2024novelaluminumalloy pages 4-6)

## Defense: qualification frameworks and material-property gates (limited component evidence)
### Defense airworthiness and DADT-centric qualification expectations
Defense-related qualification/certification emphasis in the retrieved evidence centers on **durability and damage tolerance (DADT)** and airworthiness framework alignment.

A Scalmalloy/AM crack-growth paper cites defense/airworthiness framework documents as relevant to certification (JSSG2006, MIL-STD-1530D, USAF Structures Bulletin EZ-19-01) and notes US Army directives promoting advanced manufacturing adoption across life-cycle. (jones2021characterisingcrackgrowth pages 1-3)

### Defense-relevant alloy capability thresholds: Scalmalloy®
The same source provides explicit **material capability values** that serve as gates to replace conventional high-strength aluminum alloys:
* yield strength ≈ **450 MPa**
* elongation **>10%**
* compared as similar to AA7075-T7351 and AA7050-T7451. (jones2021characterisingcrackgrowth pages 1-3)

While this supports the “property requirements enabling transition,” the retrieved corpus does not identify a specific defense production-qualified AM aluminum component with a published tensile/fatigue acceptance test matrix analogous to the aerospace manifold case. (huning2021digitalplatforminformed pages 17-19)

## Summary table of cases (evidence-based)
| Domain | Organization/program | Component | AM process | Alloy | Property thresholds/values reported (YS/UTS/El/fatigue) | Key qualification/QA standards and tests | Replaced conventional part? | Notes/limitations |
|---|---|---|---|---|---|---|---|---|
| Aerospace | NASA / NASA-wide standards | Cross-cutting pathway for spaceflight LPBF parts | LPBF metals | Alloy-specific MPS/QMP; applicable to Al alloys as well as others | Explicit acceptance examples in NASA pathway: local plastic strain `< 0.005`; HCF improved surfaces: additional life factor or `20% below required fatigue limit cyclic stress range`; HCF as-built surfaces: additional life factor or `40% below required fatigue limit cyclic stress range` (russell2019nasa’splansfor pages 2-5) | MSFC-STD-3716 / MSFC-SPEC-3717 framework: Materials Property Suite (MPS), Qualified Metallurgical Process (QMP) per machine/alloy, witness specimens for tensile/ductility/fatigue, Part Production Plan (PPP), requirements matrix by part class, comprehensive NDE for higher classes (russell2019nasa’splansfor pages 2-5, o’brien2019developmentandqualification pages 7-8, russell2019qualificationandcertification pages 25-27) | Not a single component case | NASA evidence is pathway-focused rather than giving aluminum-part-specific YS/UTS/El allowables |
| Aerospace | ESA / CATEC / PROBA-3 | Helix antenna | LPBF | AlSi10Mg | No part-specific YS/UTS/El reported in case study; acceptance driven by defect detectability and CT resolution. Supportive alloy context: LPBF AlSi10Mg fatigue strength reported at `92 ± 15 MPa` (T5-RT) and `108 ± 5 MPa` (T6R-RT); broader review reports UTS roughly `267–493 MPa`, elongation about `3.5–13.4%`, fatigue strength up to `~120 MPa` (galleguillos2023ndtforqualification pages 1-4, egidio2023roomandhightemperature pages 7-9, wang2024areviewon pages 9-11) | ECSS-Q-ST-70-80C requires CT for critical structural/functional components; CT per ASTM E1570-19 and ISO 15708-3; Airbus AIMS03-22-000 defect-size examples: `200 µm` for structural/fatigue-critical, `500 µm` for non-structural/non-fatigue; PROBA-3 antenna inspected at `64 µm` voxel size (galleguillos2023ndtforqualification pages 1-4) | Not stated | Strong example of flight hardware qualification by NDT, but no explicit tensile-property threshold published in the case paper |
| Aerospace | ESA / CATEC / JUICE | Monitoring camera bracket (JMC) | LPBF | Scalmalloy® | Scalmalloy supportive context: yield `~450 MPa`, elongation `>10%`; crack-growth threshold `ΔKthr = 1.38 MPa√m` at `R=0.1` and `0.83 MPa√m` at `R=0.7` (jones2021characterisingcrackgrowth pages 1-3, jones2021characterisingcrackgrowth pages 3-6) | Flight-hardware CT/NDT pathway under ECSS-Q-ST-70-80C; end-user safety classification sets acceptance; CT operation/evaluation per ASTM E1570-19 / ISO 15708-3; defect detectability established using IQIs with `100–1000 µm` holes (galleguillos2023ndtforqualification pages 1-4) | Not stated | Flight component explicitly documented; mechanical-property values come from supportive Scalmalloy paper, not from the JUICE bracket inspection report |
| Aerospace | Clean Sky 2 / CATEC | Fairings for CS2 demonstrator | LPBF | Scalmalloy® | No fairing-specific YS/UTS/El/fatigue reported; supportive Scalmalloy values as above (`~450 MPa` YS, `>10%` elongation) (galleguillos2023ndtforqualification pages 1-4, jones2021characterisingcrackgrowth pages 1-3) | Same NDT route: CT preferred for critical AM aerospace parts; ASTM E1570-19 / ISO 15708-3; Airbus AIMS03-22-000 defect acceptance examples `200/500 µm` (galleguillos2023ndtforqualification pages 1-4) | Not stated | Aerospace production-demonstrator case; evidence is inspection/qualification-centric |
| Aerospace | AIDRO / Chalmers / Magnaghi Aeronautica | Hydraulic manifold | LPBF (EOS M290) | forAM® Al-HS1 | Yield strength increased from `~250 MPa` as-printed to `~350 MPa` after heat treatment (`375 °C`); density `>99.7%`; fatigue qualification by four-point bending, fully reversed `R = -1`, staircase method, run-out `2×10^6` cycles; UTS/fatigue life said comparable to AlSi10Mg but not numerically listed (arena2024novelaluminumalloy pages 4-6, arena2024novelaluminumalloy pages 11-14) | Qualification matrix included proof pressure `1.5× DOP` for `2 min`, burst `2.5× DOP`, endurance/cyclic tests (`5,000` cycles functional window; SAE ARP1383 notes `100,000` cycles for utility valves), dye penetrant + UV inspection, MIL-PRF-5606J fluid, NAS 1638 class 7 contamination requirement (arena2024novelaluminumalloy pages 11-14) | Not explicitly stated | Strong production-qualification example for AM Al alloy, but not directly NASA/ESA/Airbus/Boeing |
| Aerospace | Aircraft bracket demonstrator | Topology-optimized aircraft bracket | SLM / LPBF | AlSi10Mg context | Measured full-load elongation `0.65 mm`; fatigue test at `R=0.1`, `20 Hz`, survived about `4.67 million` cycles before failure after restart; one related AlSi10Mg surface-fatigue study reports material yield strength `Rp0.2 = 212 MPa` (klippstein2019developmentproductionand pages 11-14, sausto2022analysisoffatigue pages 7-9) | Static + HCF testing; SEM fracture analysis identified pores/unmolten particles; authors concluded civil-aviation material/process qualification still required before flight use (klippstein2019developmentproductionand pages 11-14) | Intended to replace/optimize a bracket, but flight replacement not achieved in evidence shown | Useful as transition-stage evidence showing why fatigue/process control had to mature before certified use |
| Aerospace / Defense aviation | Leonardo / C-27J | Main landing gear bracket spare-part study | LPBF (EOS M270) | AlSi10Mg substituted for original conventional alloy | Numeric thresholds not reported; thesis states LPBF materials showed better mechanical properties than wrought counterparts and were tested against design requirements (pochettino2024producingaircraftmetallic pages 1-5) | Stress-relief and aging, metallography, porosity and microstructure checks, dimensional/surface-roughness checks, standard tensile specimens; positioned to support Leonardo certification path (pochettino2024producingaircraftmetallic pages 1-5) | Yes—AM AlSi10Mg explored because conventional alloy was unsuitable for LPBF (pochettino2024producingaircraftmetallic pages 1-5) | Valuable defense/aerospace sustainment case, but lacks published YS/UTS/El/fatigue numbers |
| Automotive | High-performance/student racing example | Clutch lever | SLM | AlSi10Mg | Validation threshold referenced against yield limit `220 MPa`; safety factor maintained `>3.0`; under ~`1.5×` assumed load, max von Mises stress remained below yield limit; no fatigue limit reported (mikulikova2023topologyoptimizationof pages 1-2) | FEM before/after topology optimization plus experimental bench validation; mass reduction ~`10%`; part consolidated from prior arrangement into single AM component (mikulikova2023topologyoptimizationof pages 1-2) | Yes—replaced previous part in the racing car system (mikulikova2023topologyoptimizationof pages 1-2) | Not Formula 1/OEM production, but best in-context automotive case with explicit mechanical acceptance criterion |
| Automotive | Formula 1 / Mahle Powertrain (review mention) | Pistons | Metal AM (review-level mention) | AlSi10Mg | No numeric YS/UTS/El/fatigue thresholds in the retrieved evidence; only that AlSi10Mg has been successfully used for Formula 1 pistons (arena2024novelaluminumalloy pages 4-6) | Qualification/test route not provided in retrieved context | Likely replacement of conventional pistons, but not documented in detail in context | Mentioned only in review/narrative evidence; insufficient for detailed qualification claims |
| Defense | US Army / broader military airworthiness context | Airworthiness pathway for AM Al parts | Cross-cutting | Scalmalloy and AM Al alloys broadly | Reported Scalmalloy mechanical capability: yield `~450 MPa`, elongation `>10%`, with properties comparable to AA7075-T7351/AA7050-T7451; emphasis on durability and damage tolerance (DADT) rather than fixed part-level thresholds (jones2021characterisingcrackgrowth pages 1-3) | Cited defense/airworthiness framework references: US Army Directives 2019-19 and 2019-29, JSSG2006, MIL-STD-1530D, USAF Structures Bulletin EZ-19-01; DADT assessment called essential for AM certification (jones2021characterisingcrackgrowth pages 1-3) | Potentially yes, because properties are compared to legacy high-strength aerospace Al alloys | Defense evidence is framework/material-property focused; no single qualified AM aluminum defense component with full test matrix was retrieved |


*Table: This table compiles the strongest in-context case studies and standards showing how AM aluminum and aluminum-family alloys have moved toward flight, production, or defense use. It highlights reported property values, defect acceptance criteria, and the qualification workflows that mattered most, while flagging where the evidence is still pathway-level rather than part-specific.*

## Key takeaways: what actually enables AM Al alloys to move into production
1. **A controlled process definition + traceability (QMP/MPS/PPP + witness coupons)** is the core pathway for moving beyond R&D, exemplified in NASA’s MSFC-derived framework. (russell2019nasa’splansfor pages 2-5, o’brien2019developmentandqualification pages 7-8)
2. **Defect acceptance criteria (especially CT-based) become a de facto mechanical-property protector**, particularly for fatigue-limited aluminum AM parts; ECSS-Q-ST-70-80C and Airbus AIMS03-22-000 provide concrete inspection requirements and defect-size classes (e.g., 200 µm for fatigue-relevant structural parts). (galleguillos2023ndtforqualification pages 1-4)
3. **Mechanical property gates are often expressed as either** (a) explicit yield/ductility targets at coupon level (e.g., Scalmalloy ~450 MPa yield and >10% elongation), or (b) fatigue design/acceptance margins (e.g., 20%/40% below required fatigue limit cyclic stress range in NASA’s criteria). (jones2021characterisingcrackgrowth pages 1-3, russell2019nasa’splansfor pages 2-5)
4. **Production qualification is application-specific**, often combining classical qualification tests (proof/burst pressure, endurance cycles) with AM-specific NDI and process monitoring; the Al-HS1 manifold case provides a clear example of such a test matrix. (arena2024novelaluminumalloy pages 11-14, arena2024novelaluminumalloy pages 4-6)

## Process-form gap: why LPBF — and not DED/WAAM/EBM — has reached deployment, and where ultrasonic atomization fits

All confirmed downstream deployments of AM aluminum alloys identified in this corpus use **powder-bed laser fusion (LPBF/SLM/PBF-LB/M)**. No deployed components were found for powder-blown DED, WAAM, or EBM in aluminum. The detailed evidence and quantitative comparisons are compiled in `lpbf_vs_ded_rationale.md`; the key reasons are summarized here because they directly motivate FLAIME's choice of LPBF + ultrasonic atomization rather than DED-class processes.

### Why LPBF (not DED/WAAM/EBM) for high-performance Al
* **Resolution and surface finish**: LPBF achieves ~10–50 µm layers and ~75–100 µm minimum feature size with as-built precision down to ~0.05 mm; DED layers are ~100–500 µm with poor as-deposited surface (post-machining required), WAAM operates at multi-mm bead scale, and EBM-Al lacks both the resolution and the alloy breadth of LPBF.
* **Cooling rate and microstructural refinement**: LPBF delivers ~10⁴–10⁶ K/s, producing ~500 nm cellular structures and ~10 µm grains that are unavailable to DED (~10²–10³ K/s, dendritic 10–100 µm) or WAAM (10¹–10² K/s, coarse columnar). The fine cellular Si network underlies the favorable strength-ductility envelope of LPBF AlSi10Mg.
* **Alloy compositional flexibility via rapid solidification**: LPBF's high cooling rates enable Sc/Zr-bearing precipitation systems (Scalmalloy, Al-Mn-Sc-Zr), TiB₂-refined high-strength systems (A20X), and other supersaturated chemistries that solidify with cracking and segregation in DED/WAAM.
* **Defects and process windows**: WAAM-Al is dominated by H-driven porosity from arc/wire chemistry; DED-Al inherits welding-class oxide entrapment and lack-of-fusion. LPBF's enclosed inert chamber, narrow melt pool, and per-track parameter control give it the smallest aluminum-specific defect window of the four processes.
* **Qualification ecosystem**: NASA MSFC, ECSS-Q-ST-70-80, and Airbus AIMS frameworks for AM aluminum are all built around PBF-LB; DED/WAAM/EBM-Al qualification standards for safety-critical structural use are not yet mature.

### Why ultrasonic atomization (not gas atomization or wire) for novel-composition powder
* **Particle size envelope matched to LPBF**: Ultrasonic atomization (e.g., AMAZEMET rePOWDER) produces the fine, narrow PSD (D₅₀ in the ~20–45 µm window) that LPBF requires for thin layers and good packing density; gas atomization yields broader distributions requiring downstream sieving and yield loss.
* **Small-batch novel chemistries**: Gas atomization typically requires kilogram-to-tonne batches; ultrasonic atomization can produce gram-to-kilogram batches per run with rapid composition turnover, enabling closed-loop alloy discovery where each design iteration consumes <1 kg of feedstock. This is a hard prerequisite for high-throughput Bayesian alloy search across a 15-element composition space.
* **Wire vs. powder for alloy discovery**: Wire feedstock (used in WAAM, wire-DED) constrains compositions to whatever is commercially extruded as wire — typically only 4xxx, 5xxx, and a few weldable 2xxx grades. Powder feedstock — and especially elemental-blend or ultrasonically atomized prealloy — lifts that constraint and is what enables alloy compositions to be designed rather than selected.
* **Low-oxygen, spherical morphology**: Ultrasonic atomization of pre-alloyed feedstock under inert atmosphere maintains the low O/H content (<500 ppm O typical) and high sphericity that LPBF requires; AMC composites and refractory-matrix systems have been demonstrated.

The collective evidence is that **LPBF is the only AM process where aluminum alloys have crossed from R&D into named OEM deployments**, and **ultrasonic atomization of small-batch novel compositions is the only feedstock route that lets new alloys feed that pipeline at the iteration cadence that AI-driven discovery requires**. Wire-based DED would constrain FLAIME to compositions that are already drawn as wire; conventional gas atomization would constrain FLAIME to compositions justified by kg-scale batch economics. Neither pathway is compatible with high-throughput discovery of genuinely novel Al chemistries for printing.

## Caveat: corrosion is a real, alloy- and process-dependent risk for LPBF Al

A separate Edison query (`corrosion_performance.md`, task `1aa0d65b`) compiles the corrosion evidence for LPBF aluminum vs wrought equivalents and cautions that **LPBF aluminum corrosion performance is not uniform and can be worse than wrought**, particularly when (i) surface-connected porosity and as-built roughness expose subsurface defects, (ii) melt-pool boundaries concentrate segregation or oxide skins, and (iii) heat treatment coarsens or redistributes galvanic phases (for example, breakdown of the cellular Si network in T6 AlSi10Mg, or copper-rich precipitates and PFZs in Al–Cu systems). Reported behaviors range from **modest LPBF improvements over wrought** (some 7xxx/2xxx LPBF systems with refined cathodic constituents) to **substantially worse pitting/IGC/SCC** (heat-treated AlSi10Mg, Al–Cu–Li after specific T8x cycles, surface-exposed melt-pool networks). Mitigations documented in the literature include HIP, optimized surface machining, anodizing, controlled aging cycles, and alloy-design choices that avoid coarse galvanic networks.

The practical implication is that for downstream applications such as **automotive structural castings (e.g., Divergent Adaptive Production System, mentioned in current industry hiring for materials/corrosion engineers)**, corrosion screening must be treated as a first-class property axis alongside YS/UTS/elongation/fatigue when ranking candidate AM Al chemistries. This argues for adding NaCl immersion / potentiodynamic / salt-spray screening into FLAIME's downstream characterization pipeline for any composition that is being considered for non-aerospace structural applications.

## Notable gaps vs. the user request
Within the retrieved full text, I could not extract:
* Airbus- or Boeing-issued minimum tensile/fatigue allowables for specific flight-qualified AM aluminum parts (YS/UTS/El/fatigue limits),
* a Boeing production-qualified AM aluminum component with published mechanical thresholds,
* an OEM automotive production case (non-motorsport) with published tensile/fatigue acceptance thresholds and a formal qualification route,
* a defense production-qualified AM aluminum component with a published, complete mechanical acceptance test matrix.

These gaps reflect lack of accessible internal OEM specifications and limited open literature reporting of certified part allowables rather than an absence of real-world deployments.

References

1. (russell2019nasa’splansfor pages 2-5): Richard Russell. Nasa’s plans for development of a standard for additively manufactured components. Journal of Materials Engineering and Performance, 28:1924-1928, Mar 2019. URL: https://doi.org/10.1007/s11665-019-03939-x, doi:10.1007/s11665-019-03939-x. This article has 9 citations and is from a peer-reviewed journal.

2. (galleguillos2023ndtforqualification pages 1-4): Carlos Galleguillos, Antonio Periñán, Sergio González, and Fernando Lasagni. Ndt for qualification of space hardware made by additive manufacturing. Research and Review Journal of Nondestructive Testing, Aug 2023. URL: https://doi.org/10.58286/28124, doi:10.58286/28124. This article has 1 citations.

3. (galleguillos2023ndtforqualification media 19ce40e6): Carlos Galleguillos, Antonio Periñán, Sergio González, and Fernando Lasagni. Ndt for qualification of space hardware made by additive manufacturing. Research and Review Journal of Nondestructive Testing, Aug 2023. URL: https://doi.org/10.58286/28124, doi:10.58286/28124. This article has 1 citations.

4. (egidio2023roomandhightemperature pages 7-9): Gianluca Di Egidio, Lorella Ceschini, Alessandro Morri, and Mattia Zanni. Room- and high-temperature fatigue strength of the t5 and rapid t6 heat-treated alsi10mg alloy produced by laser-based powder bed fusion. Metals, 13:263, Jan 2023. URL: https://doi.org/10.3390/met13020263, doi:10.3390/met13020263. This article has 15 citations.

5. (jones2021characterisingcrackgrowth pages 1-3): Rhys Jones, Jan Cizek, Ondrej Kovarik, Jeff Lang, Andrew Ang, and John G. Michopoulos. Characterising crack growth in scalmalloy. Procedia Structural Integrity, 34:39-44, Jan 2021. URL: https://doi.org/10.1016/j.prostr.2021.12.006, doi:10.1016/j.prostr.2021.12.006. This article has 1 citations and is from a peer-reviewed journal.

6. (arena2024novelaluminumalloy pages 11-14): Maurizio Arena, Bharat Mehta, Tommaso Tirelli, Paolo Ambrogiani, Martina Castaldo, Sven Bengtsson, and Lars Nyborg. Novel aluminum alloy tailored for additive manufacturing: structural characterization and qualification perspectives. Applied Sciences, 14:4647, May 2024. URL: https://doi.org/10.3390/app14114647, doi:10.3390/app14114647. This article has 0 citations.

7. (arena2024novelaluminumalloy pages 4-6): Maurizio Arena, Bharat Mehta, Tommaso Tirelli, Paolo Ambrogiani, Martina Castaldo, Sven Bengtsson, and Lars Nyborg. Novel aluminum alloy tailored for additive manufacturing: structural characterization and qualification perspectives. Applied Sciences, 14:4647, May 2024. URL: https://doi.org/10.3390/app14114647, doi:10.3390/app14114647. This article has 0 citations.

8. (mikulikova2023topologyoptimizationof pages 1-2): Aleksandra Mikulikova, Jakub Mesicek, Jan Karger, Jiri Hajnys, Quoc-Phu Ma, Ales Sliva, Jakub Smiraus, David Srnicek, Samuel Cienciala, and Marek Pagac. Topology optimization of the clutch lever manufactured by additive manufacturing. Materials, 16:3510, May 2023. URL: https://doi.org/10.3390/ma16093510, doi:10.3390/ma16093510. This article has 18 citations.

9. (huning2021digitalplatforminformed pages 17-19): Alex Huning, Randall Fair, Alyson Coates, Vincent Paquit, Luke Scime, Michael Russell, Kenneth Kane, Samuel Bell, Bruce Lin, and Benjamin Betzler. Digital platform informed certification of components derived from advanced manufacturing technologies. ArXiv, Sep 2021. URL: https://doi.org/10.2172/1824955, doi:10.2172/1824955. This article has 11 citations.

10. (o’brien2019developmentandqualification pages 7-8): Michael James O’Brien. Development and qualification of additively manufactured parts for space. Optical Engineering, 58:1, Jan 2019. URL: https://doi.org/10.1117/1.oe.58.1.010801, doi:10.1117/1.oe.58.1.010801. This article has 35 citations and is from a peer-reviewed journal.

11. (russell2019qualificationandcertification pages 25-27): Richard Russell, Douglas Wells, Jess Waller, Behrang Poorganji, Eric Ott, Tsuyoshi Nakagawa, Hector Sandoval, Nima Shamsaei, and Mohsen Seifi. Qualification and certification of metal additive manufactured hardware for aerospace applications. Additive Manufacturing for the Aerospace Industry, pages 33-66, Jan 2019. URL: https://doi.org/10.1016/b978-0-12-814062-8.00003-0, doi:10.1016/b978-0-12-814062-8.00003-0. This article has 139 citations.

12. (wang2024areviewon pages 9-11): Xin Wang, Dongyun Zhang, Ang Li, Denghao Yi, and Tianci Li. A review on traditional processes and laser powder bed fusion of aluminum alloy microstructures, mechanical properties, costs, and applications. Materials, 17:2553, May 2024. URL: https://doi.org/10.3390/ma17112553, doi:10.3390/ma17112553. This article has 39 citations.

13. (jones2021characterisingcrackgrowth pages 3-6): Rhys Jones, Jan Cizek, Ondrej Kovarik, Jeff Lang, Andrew Ang, and John G. Michopoulos. Characterising crack growth in scalmalloy. Procedia Structural Integrity, 34:39-44, Jan 2021. URL: https://doi.org/10.1016/j.prostr.2021.12.006, doi:10.1016/j.prostr.2021.12.006. This article has 1 citations and is from a peer-reviewed journal.

14. (klippstein2019developmentproductionand pages 11-14): Helge Klippstein, Anne Duchting, Thomas Reiher, Florian Hengsbach, Dennis Menge, and Hans-Joachim Schmid. Development, production and post-processing of a topology optimized aircraft bracket. Unknown, Jan 2019. URL: https://doi.org/10.26153/tsw/17448, doi:10.26153/tsw/17448. This article has 9 citations.

15. (sausto2022analysisoffatigue pages 7-9): Francesco Sausto, Christian Tezzele, and Stefano Beretta. Analysis of fatigue strength of l-pbf alsi10mg with different surface post-processes: effect of residual stresses. Metals, 12:898, May 2022. URL: https://doi.org/10.3390/met12060898, doi:10.3390/met12060898. This article has 45 citations.

16. (pochettino2024producingaircraftmetallic pages 1-5): A Pochettino. Producing aircraft metallic spare parts by additive manufacturing to enhance logistic support. Unknown journal, 2024.