# Literature Search: LPBF Superalloy Powders

*Edison Scientific LITERATURE_HIGH query + web search synthesis*

Question: What is the published literature on next-generation nickel superalloy powders designed specifically for laser powder bed fusion (LPBF) additive manufacturing? Cover the following alloy systems: (1) GE Aerospace A94 and A115, (2) ABD-900AM by Alloyed (formerly OxMet Technologies), (3) GammaPrint by Carpenter Technology, (4) ATI 1700 by ATI Specialty Metals, and (5) NASA GRX-810. For each alloy, address composition, gamma prime characteristics, mechanical properties, printability, and scaling considerations. Also cover key strengthening mechanisms: gamma prime quantity, gamma prime solvus, solid solution strengthening, and corrosion resistance.

Context: Notes from a talk by Laura Dial at GE Aerospace Research (TMS 2026 keynote), covering the competitive landscape of LPBF-specific nickel superalloy powders.

---

## 1. GE Aerospace A94 and A115

### 1.1 Overview

GE Aerospace has developed two proprietary nickel-based superalloy compositions—**A94** and **A115**—specifically designed for laser powder bed fusion (LPBF) additive manufacturing of hot-section turbine engine components. These alloys represent GE's strategy to move beyond legacy AM alloys (IN718, CoCr, Hastelloy X) into the high-temperature regime previously reserved for cast-and-wrought superalloys.

Laura Dial, a principal scientist in GE Aerospace Research's Materials and Manufacturing Technologies Organization, presented on these alloys as part of a keynote at TMS 2026 titled "Advancing High-Temperature Alloys for Aerospace Applications: A Survey of Nickel Based Superalloys for Laser Powder Bed Fusion, Including Innovations at GE Aerospace" ([ProgramMaster abstract](https://programmaster.org/PM/PM.nsf/ApprovedAbstracts/BB639FE8CB4AE9C485258CC7006FC05F)).

**Note on public availability (confirmed by Edison Scientific LITERATURE_HIGH search):** No publicly available documentation specifically describing GE Aerospace nickel superalloy compositions designated as "A94" and "A115" was found in academic databases, patent literature, or conference proceedings. These appear to be internal/proprietary alloy designations that have not yet been disclosed in accessible scientific literature as of early 2026. The information below is drawn from Laura Dial's TMS 2026 keynote presentation and related public disclosures.

### 1.2 A94 — Intermediate Temperature (650–780°C)

- **Target service temperature**: 650–780°C
- **Strengthening mechanism**: Gamma-prime (γ') precipitation strengthening
- **Positioning**: Designed to surpass cobalt-chrome alloys and Alloy 718 in strength and low-cycle fatigue (LCF) performance at intermediate temperatures
- **Key properties of interest**: Tensile strength, LCF life
- **Design philosophy**: Engineered for LPBF printability with controlled γ' content to balance cracking resistance with high-temperature capability
- **Powder characteristics**: Gas-atomized, high sphericity, controlled particle size distribution, low oxygen pickup

### 1.3 A115 — High Temperature (780–880°C)

- **Target service temperature**: 780–880°C
- **Strengthening mechanism**: γ'-strengthened with high volume fraction precipitates
- **Target applications**: Combustor components requiring combined LCF, HCF, oxidation resistance, and hot corrosion resistance
- **Key properties of interest**: Low-cycle fatigue (LCF), high-cycle fatigue (HCF), oxidation resistance, hot corrosion resistance
- **Design philosophy**: Higher γ' content than A94, designed for aggressive thermal environments

### 1.4 Scaling Considerations (GE)

GE has demonstrated A94 and A115 on a **500 mm × 500 mm build platform** using GE's large-format LPBF printer (Colibrium Additive). Key scaling challenges identified include:

- **Recrystallization**: Post-processing heat treatments must be carefully controlled to manage recrystallization in large builds with complex thermal histories
- **Cooling rate sensitivity**: Larger build volumes result in varying cooling rates across the part, affecting γ' precipitation kinetics and final properties
- **Age cycle optimization**: Time and temperature sensitivity of the aging cycle must account for thermal gradients in large parts
- **Compatibility**: Alloys must be compatible with downstream processes including brazing, welding, and protective coatings for integration into turbine assemblies

### 1.5 GE's Documented LPBF Superalloy Programs

GE Aviation/GE Additive have an extensive, well-documented LPBF superalloy development portfolio that contextualizes A94 and A115:

**Alloy 718 LPBF (Kelkar et al. 2018):** GE's most mature LPBF superalloy program. Demonstrated yield strength ~10% below wrought but ~50% above cast; UTS approaching wrought; LCF better than cast and approaching wrought; crack growth similar to wrought. Multi-step heat treatment: stress relief → HIP → solution treatment near delta solvus (997–1032°C) → standard aging (718°C + 621°C, 8 h each). Qualified for ATP engine exhaust case, C-sump, and propeller gearbox housing. Evolution from 20 μm to 50 μm layers improved productivity, as reported by Kelkar et al. (2018).

**CoCrMo (LEAP fuel nozzle):** GE's pioneer qualified flying metal-AM part — the LEAP fuel nozzle. Established GE's LPBF manufacturing framework and quality systems.

**High γ' Superalloy Platform (EP4559598A1, 2025):** A key European patent filed by Concept Laser GmbH and Arcam AB (both GE Additive companies) discloses AM processes for superalloys with γ' ≥ 35 vol%, addressing cracking in "non-weldable" alloys. Mentions Rene 108, Rene N5, GTD 111, GTD 444, MarM 247, CM247LC, and IN 738 as candidate alloys. Enables controlled microstructure evolution to produce equiaxed polycrystalline, directionally solidified (DS), or even single-crystal (SX) microstructures within a single AM article. This patent likely represents the technology platform underlying A94 and A115 development.

### 1.6 Laura Dial and GE Research Publications

Laura Dial is a principal scientist in GE Aerospace Research's Materials and Manufacturing Technologies Organization with >15 years of experience in metallic materials R&D. Key identified publications:

1. Shukla, A., Sarkar, S., Durga, A., Adharapurapu, R., **Dial, L.**, and Sondhi, S.K. "Computational design of additively printable nickel superalloys." *Proceedings of Superalloys 2020*, pp. 1066–1074 (2020).
2. Wessman, A., Cormier, J., Hamon, F., Rainey, K., Tin, S., Tiparti, D., and **Dial, L.** "Microstructure and mechanical properties of additively manufactured Rene 65." *Proceedings of Superalloys 2020*, pp. 961–971 (2020).
3. NSF-funded collaboration ($1.97M, 2023) with Ohio State University, NASA Glenn Research Center, and AFRL on oxide-dispersion strengthened (ODS) superalloys for AM.

### 1.7 Related Programs

- **Colibrium Additive** (GE Aerospace company): Provides both large-format LPBF printers and specialty superalloy powders for aerospace AM

### 1.8 Key References

- Dial, L. "Advancing High-Temperature Alloys for Aerospace Applications: A Survey of Nickel Based Superalloys for Laser Powder Bed Fusion, Including Innovations at GE Aerospace." TMS 2026 Additive Manufacturing Keynote Session.
- Kelkar, R. et al. "Alloy 718 Laser Powder Bed Fusion AM for GE Aviation." *Proceedings of 9th Intl Symposium on Superalloy 718 & Derivatives* (2018).
- EP4559598A1, "Methods of Manufacturing Superalloy Articles." Concept Laser GmbH / Arcam AB (2025).
- [Colibrium Additive](https://colibriumadditive.com) — GE's AM powder and printer platform
- Progress in additive manufacturing of nickel-based superalloys, *Rare Metals* (2025), Springer. doi:10.1007/s12598-025-03247-5
- Srinivasan & Ananth, "Recent Advances in Superalloy AM" (2022).

---

## 2. ABD-900AM by Alloyed (formerly OxMet Technologies)

### 2.1 Overview

ABD-900AM is a precipitation-hardened, nickel-based superalloy designed from the ground up for crack-free additive manufacturing via LPBF. It was developed by **Alloyed** (formerly OxMet Technologies), a spinout from the University of Oxford founded on the computational alloy design methodology pioneered by **Professor Roger Reed**. The company's proprietary **Alloys-by-Design (ABD®)** platform uses ICME (Integrated Computational Materials Engineering) to computationally optimize alloy compositions for both printability and service performance.

Note: The initial research request referenced "ABD 800 AM" — this likely refers to ABD-900AM, which targets the 800–900°C service temperature regime. The ABD family also includes ABD-850AM (~600°C) and ABD-1000AM (>1000°C).

### 2.2 Alloy Composition

Published nominal composition (wt%) from Tang et al. (2021), *Acta Materialia* 202:417–436 (doi:10.1016/j.actamat.2020.09.023, 644 citations):

| Element | wt% | at% (approx.) | Role |
|---------|-----|---------------|------|
| Ni | Balance | — | Matrix |
| Cr | 17.0 | — | Oxidation/corrosion resistance |
| Co | 19.9 | — | Solid solution strengthening, phase stability |
| W | 3.1 | — | Solid solution strengthening |
| Al | 2.1 | ~4.5 | γ' former (Ni₃Al) |
| Ti | 2.4 | ~2.9 | γ' former (Ni₃(Al,Ti)) |
| Mo | 2.1 | — | Solid solution strengthening |
| Nb | 1.8 | — | γ' and δ strengthening |
| Ta | 1.4 | — | γ' strengthening, solid solution |
| C | 0.05 | — | Carbide formation |
| B | 0.005 | — | Grain boundary strengthening |

(Sources: Tang et al. 2021 *Acta Materialia*; OxMet Technologies datasheet; Aubert & Duval Stellar ABD-900AM product sheet)

### 2.3 Gamma Prime Characteristics

- **γ' volume fraction**: ~35% in the age-hardened condition (comparable to IN939/IN738)
- **γ' solvus temperature**: ~1056°C (Thermo-Calc TCNI8 prediction) / ~1079°C (DSC onset measurement) (Zhuge et al. 2026, *Metallurgical and Materials Transactions A*, doi:10.1007/s11661-025-08081-z)
- **Microstructure**: Fine γ' precipitates in a stable γ matrix, designed for bimodal precipitate distribution after heat treatment
- **TTT diagram**: γ' nose at ~1140 K (~867°C); precipitates form within ~5 seconds at the nose temperature
- **Coarsening kinetics**: Q = 302 ± 5 kJ/mol, exponent n ≈ 2.9 (matrix-diffusion-controlled LSW regime)
- **Peak hardness**: 480–522 HV₀.₅ at γ' median radius 10–20 nm (weak-to-strong coupling dislocation transition)
- **Early-stage morphology**: Interconnected structures at r < 6 nm, suggesting possible spinodal decomposition pathway

### 2.4 Mechanical Properties

**Room-temperature tensile properties** (orientation-dependent, Tang et al. 2020):

| Orientation | 0.2% YS (MPa) | UTS (MPa) | Elongation (%) |
|-------------|---------------|-----------|----------------|
| Horizontal | ~950 | ~1375–1421 | ~13.7–16.5 |
| Vertical | ~1007 | ~1375–1421 | ~13.7–16.5 |
| 45° | ~1059 | ~1375–1421 | ~13.7–16.5 |

**Elevated temperature properties:**

| Property | Value | Condition |
|----------|-------|-----------|
| Yield Strength | ~770–780 MPa | 900°C |
| UTS | ~840–850 MPa | 900°C |
| Elongation | 6% (XY), 17% (Z) | 900°C |
| Density | ~8.4 g/cm³ | — |
| Melting Range | 1305–1380°C | — |
| Relative Density | >99.9% | As-printed LPBF |

**Creep performance** (Bridges & Shingledecker 2025, *JOM*, doi:10.1007/s11837-025-07326-x):

- **>67,000 hours** of accumulated creep testing data (700–900°C, 100–600 MPa)
- **+125°C temperature capability advantage** vs. IN718 in creep applications
- **Super-solvus HT (HT2)**: 1240°C/2h + 1060°C/2h + 850°C/4h + 760°C/16h — markedly improves creep vs. sub-solvus treatments
- **Creep mechanisms**: At <250 MPa, MC carbides grow at GBs producing precipitate-free zones; at >250 MPa, grain-boundary cavitation dominates
- **EBPBF density**: ~98.4% as-built, improved to ~99.8% via HIP at 1120°C/100 MPa

(Sources: Tang et al. 2020 *Superalloys 2020*; OxMet Technologies ABD-900AM datasheet; Aubert & Duval; Bridges et al. 2024, 2025)

### 2.5 Printability

- **Crack-free LPBF**: ABD-900AM was the first nickel superalloy purposely designed for crack-free AM processing
- **Process compatibility**: Prints with standard IN718 LPBF parameters — no heated build plate required
- **Layer thickness**: Compatible with thick layers up to 60 μm
- **Production yields**: High, with optimized process windows avoiding solidification, liquation, and strain-age cracking
- **ABD design constraints** (Tang et al. 2021): Strain-age cracking index f(SA) = W_Al + 0.5W_Ti + 0.3W_Nb + 0.15W_Ta ≤ 3–4 wt%; freezing range ≤ 280 K (Scheil); >10⁷ trial compositions screened
- **Defect comparison**: CM247LC crack density ~1.3 mm/mm² vs. ABD-850AM ~0.01 mm/mm² (Ghoussoub et al. 2022)

**LPBF processing parameters** (Ghoussoub et al. 2022; Zhuge et al. 2026):

| Parameter | Value |
|-----------|-------|
| Machine | Renishaw AM 400/AM 500Q |
| Laser power | 200 W |
| Spot size | ~70 µm |
| Layer thickness | 30 µm |
| Scan speed | ~0.875 m/s (hatch), ~0.5 m/s (border) |
| Hatch spacing | ~70 µm |
| Scan strategy | Meander with 67° layer rotation |
| Powder D₅₀ | 32–37 µm (D₁₀–D₉₀: 19–56 µm) |

### 2.6 ABD Alloy Family

| Alloy | Max Service Temp | γ' Solvus | γ' Fraction | Key Applications |
|-------|-----------------|-----------|-------------|------------------|
| ABD-850AM | ~600°C | ~1040°C | ~20 mol% (900°C) | Structural components |
| ABD-900AM | ~900°C | ~1056–1079°C | ~35% | Turbines, combustors, rockets |
| ABD-1000AM | >1000°C | Not disclosed | Higher | Next-gen jet engines, turbine blades |

**ABD-850AM composition (wt%)**: Ni-bal, 1.5 Al, 18.0 Co, 20.0 Cr, 2.0 Mo, 0.5 Nb, 0.5 Ta, 2.5 Ti, 5.0 W, 0.04 C, 0.005 B. Porosity ~0.10%, crack density ~0.01 mm/mm². Creep: 77 h at 700°C/600 MPa; 15.9 h at 800°C/400 MPa; 12.9 h at 900°C/200 MPa (Clark et al. 2019).

**ABD-1000AM** was co-developed with **Aubert & Duval** and achieves crack-free AM processing with stress rupture lives comparable to cast Ni247LC (launched June 2024). Compositional ranges (wt%): Al ~4–6, Co ~8–15, Cr ~6–15, W ~4.7–10.7. LPBF density >99.9%, max pore size ~50 µm, crack density <0.1 mm/mm² (Peachey et al. 2024).

### 2.7 Oxidation Behavior

At 1000°C (Ghoussoub et al. 2023, *Met. Mat. Trans. A*, doi:10.1007/s11661-022-06860-6):

- **Oxide scale**: Outer TiO₂ + continuous inner Cr₂O₃; discontinuous Al₂O₃ beneath (insufficient Al for continuous alumina at ~4.5 at%)
- **Subscale**: TiN and AlN precipitates from nitrogen ingress (Ti > 2.7 at% threshold)
- **Design trade-off**: Al > 9–11.5 at% needed for continuous Al₂O₃, but this worsens printability — ABD-900AM is a chromia-forming alloy by design

### 2.8 Key References

- Tang, Y.T. et al. "Alloys-by-design: Application to new superalloys for additive manufacturing." *Acta Materialia*, 202:417–436 (2021). doi:10.1016/j.actamat.2020.09.023 *(644 citations — foundational ABD methodology paper)*
- Tang, Y.T. et al. "The effect of heat treatment on tensile yielding response of the new superalloy ABD-900AM for additive manufacturing." *Superalloys 2020 (Springer)*, pp. 1055–1065 (2020). doi:10.1007/978-3-030-51834-9_103 *(47 citations)*
- Ghoussoub, J.N. et al. "On the influence of alloy composition on the additive manufacturability of Ni-based superalloys." *Met. Mat. Trans. A*, 53:962–983 (2022). doi:10.1007/s11661-021-06568-z *(69 citations)*
- Ghoussoub, J.N. et al. "Alloy design for additive manufacturing: Early-stage oxidation of nickel-based superalloys." *Met. Mat. Trans. A*, 54:1721–1729 (2023). doi:10.1007/s11661-022-06860-6 *(23 citations)*
- Bridges, A. and Shingledecker, J. "Creep deformation and damage mechanisms in an advanced high-temperature additively manufactured nickel-base superalloy." *JOM* (2025). doi:10.1007/s11837-025-07326-x *(12 citations)*
- Bridges, A. et al. "Acceleration of material acceptance and industry adoption of an additively manufactured nickel-base superalloy." *AM-EPRI 2024*, 84871:74–87 (2024). doi:10.31399/asm.cp.am-epri-2024p0074
- Zhuge, Y. et al. "Characterization of γ' precipitation kinetics in additively manufactured Ni-based superalloy ABD®-900AM." *Met. Mat. Trans. A* (2026). doi:10.1007/s11661-025-08081-z
- Clark, J.W.G. et al. "Design of high-temperature superalloys for additive manufacturing." *2019 Joint EPRI–123HiMAT Conference*, 84680:880–891 (2019). doi:10.31399/asm.cp.am-epri-2019p0880
- Peachey, D. et al. "ABD-1000AM: A highly processible superalloy for additive manufacturing, computationally designed for 1000°C applications." *AM-EPRI 2024*, 84871:861–872 (2024). doi:10.31399/asm.cp.am-epri-2024p0861
- Panwisawas, C., et al. "Modelling of additive manufacturability of nickel-based superalloys for laser powder bed fusion." *Acta Materialia* (2022). doi:10.1016/j.actamat.2022.118369
- "Learnings in the Qualification of ABD-900AM for Turbine, Aerospace and Rocket Applications." *ASME J. Gas Turbines Power* 148(1), 011026 (2025). doi:10.1115/1.4066889
- "High-Temperature Performance Meets Printability: A Breakthrough in AM Nickel Superalloys." *Advanced Materials & Processes* 183(6), 22 (2025).
- Aubert & Duval and Alloyed Launch ABD-1000AM Nickel Superalloy (press release, June 2024).

---

## 3. GammaPrint by Carpenter Technology

### 3.1 Overview

**GammaPrint** is a family of superalloy powders developed by **Carpenter Technology Corporation** specifically for additive manufacturing via LPBF. The development was supported by the U.S. Department of Energy's **Advanced Materials & Manufacturing Technologies Office (AMMTO)** in collaboration with **Oak Ridge National Laboratory (ORNL)** and the **University of California, Santa Barbara**. The family includes:

- **GammaPrint-1100**: Nickel-based superalloy (primary composition)
- **GammaPrint-700**: CoNi-based superalloy (~equiatomic Co:Ni on atomic basis), licensed variant of the academic SB-CoNi-10 composition

### 3.2 GammaPrint-1100 Composition and Design

- **Design methodology**: CALPHAD thermodynamic modeling combined with ICME approaches
- **Composition**: Proprietary Ni-based; includes optimized levels of Ti, Al, W, Ta, Mo, Nb, Zr
- **Patent**: US20210180158A1 (N. Zhou, CRS Holdings/Carpenter Technology): Broad range: Ni ≥50 bal., Co 0–15, Al 0.5–5.5, Cr 4–16, Ta 7.5–14.5, W 0–8. Preferred: Co 9–11, Al 4–5.5, Cr 8–10, Ta 9.5–11.5, W 4–6, Mo 2–5. Constraints: Al+Ti ≤ 6 wt%, W+Mo+Ru+Re < 10 wt%, C+B+Si+Zr < 0.15 wt%.
- **Key design targets**: γ' fraction >35%, preferably >50% (examples ~60%); γ' solvus > 1121°C (2050°F); lattice misfit δ > −0.1%, preferably −0.05% to +0.6%; γ' equivalent diameter ~300–500 nm after aging

### 3.2.1 GammaPrint-700 Composition

GammaPrint-700 is a **CoNi-based** superalloy (~equiatomic Co:Ni on atomic basis), with Ta as primary γ' former (~10.5 wt%) (Raeker et al. 2023, *Met. Mat. Trans. A*, doi:10.1007/s11661-023-06957-6):

| Variant | Co (wt%) | Ni (wt%) | Al (wt%) | Cr (wt%) | Ta (wt%) | W (wt%) | C (wt%) | B (wt%) | Hf (wt%) |
|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|
| GP-700LC | Bal. | 35.88 | 5.97 | 5.27 | 10.43 | 3.03 | 0.020 | 0.013 | 0.055 |
| GP-700 | Bal. | 36.20 | 5.43 | 5.18 | 10.50 | 3.00 | 0.030 | 0.010 | 0.040 |
| GP-700C | Bal. | 35.73 | 6.00 | 5.09 | 10.61 | 3.05 | 0.073 | 0.015 | 0.080 |
| GP-700BC | Bal. | 35.73 | 6.01 | 5.07 | 10.61 | 3.06 | 0.076 | 0.029 | 0.080 |

### 3.3 Gamma Prime Characteristics

- **GammaPrint-1100**: γ' solvus onset ~1162°C, completion ~1191°C
- **GammaPrint-700 family**: γ' volume fraction ~70% (SB-CoNi-10 family, after solution + aging); γ' solvus onset: 1196–1213°C depending on variant
- **GP-1100 patent alloy space**: γ' fraction >35%, typically ~60%
- **γ/γ' misfit**: Carefully controlled to minimize strain-age cracking; positive misfit (+0.209 to +0.294%) shown to improve AM crack resistance vs. CM247LC negative misfit (−0.035%)
- **Solvus temperature**: Designed for stability well beyond 760°C

| Variant | γ' Solvus Onset (°C) | γ' Volume Fraction |
|---------|----------------------|--------------------|
| GP-700LC | 1213 | ~70% |
| GP-700 | 1206 | ~70% |
| GP-700C | 1196 | ~70% |
| GP-700BC | 1206 | ~70% |
| GP-1100 | 1162 | ~55–60% (patent space) |

### 3.4 Mechanical Properties

| Property | Value | Condition |
|----------|-------|-----------|
| 0.2% Yield Strength | ~1100 MPa | 760°C, fully heat treated |
| Hot Ductility | >5% elongation | — |
| Stress Rupture Life | 100 hours | 207 MPa at 871°C |

- **GP-1100 temperature capability**: +133°C (240°F) vs. AM Hastelloy X for tip shoe application
- **GP-700 temperature capability**: +109°C (197°F) vs. AM Hastelloy X
- **Fatigue at 760°C**: GP-1100 exceeded Hastelloy X in both longitudinal and transverse directions; GP-700 showed significant transverse debit
- **Ductility-dip regime**: Both alloys exhibit a ductility dip above ~750°C
- Room-temperature tensile properties comparable to alloy 939
- Maintains strength at temperatures **200°C higher** than alloy 939
- Significantly outperforms LPBF Hastelloy X (the AM baseline) in strength and rupture life

(Sources: Kirka et al. 2024 ORNL Report doi:10.2172/2525861; Superalloys 2024 proceedings)

### 3.5 Printability and Process Development

- **Platform**: EOS M290 at ORNL
- **Powder size**: −53/+15 µm, produced by VIGA (vacuum induction melting inert gas atomization)
- **GP-700**: 10 builds; ORNL high-throughput parameters offered ~50% throughput increase (print time from 1 week to 3 days for tip shoe)
  - CTC parameters → "coarse" microstructure (~250 µm × 100 µm grains, strong [001] texture)
  - ORNL fast parameters → "fine" microstructure (~100 µm × 50 µm grains, weaker texture)
- **GP-1100**: 25 builds; CTC parameters remained optimal
- **Crack resistance**: Designed to be inherently resistant to solidification and strain-age cracking during LPBF
- **Boron sensitivity**: Cracking severe at B = 0.029 wt% vs. minimal at B ≤ 0.015 wt%; incipient melting drops from ~1290°C to ~1243°C with high B (Raeker et al. 2023)
- **HIP cracking issue**: GP-1100 component-scale tip shoe builds cracked during HIP; mitigated by compliant supports + on-plate HIP
- **Application demonstrations**: Turbine tip-shoe components with complex internal cooling features — components only achievable through AM
- **Post-processing**: Advanced heat treatments with controlled recrystallization to optimize microstructure

### 3.6 Academic Collaborations

- **ORNL**: Led the DOE-funded development project (PI: M.M. Kirka)
- **UC Santa Barbara**: Academic research collaboration
- **Thermo-Calc**: CALPHAD-based accelerated alloy design webinar featuring GammaPrint development
- **Carpenter Emerging Technology Center** (Alabama): Hub for AM process optimization, powder characterization, and qualification

### 3.7 Key References

- Raeker, E.B. et al. "Minor elements and solidification cracking during laser powder-bed fusion of a high γ' CoNi-base superalloy." *Met. Mat. Trans. A*, 54:1744–1757 (2023). doi:10.1007/s11661-023-06957-6 *(18 citations — GP-700 composition + cracking study)*
- Kirka, M.M. et al. "Novel hot gas components for gas turbine engines enabled by materials and additive manufacturing process development." ORNL Report (2024). doi:10.2172/2525861
- Rojas, J.O. et al. "Design of novel hot gas component for gas turbine engines enabled by materials and additive manufacturing process development." OSTI Report (2024). doi:10.2172/3002889
- Kirka, M.M. et al. "Novel Hot Gas Components for Gas Turbine Engines Enabled by Materials and Additive." ORNL publication (2023). https://www.ornl.gov/publication
- Kirka, M.M. AMMTO Peer Review Presentation (2023). https://www.energy.gov/eere
- "Design of Novel Hot Gas Component for Gas Turbine Engines Enabled by AM." OSTI (2024). https://www.osti.gov/biblio/2573311
- "Influence of the γ/γ' Misfit on the Strain-Age Cracking Resistance of..." *Superalloys 2024*, Springer, pp. 1084–1095. doi:10.1007/978-3-031-63937-1_84
- "Investigation into the Effect of Recrystallization and Microstructure on Mechanical Properties of GammaPrint-1100." TMS 2024.
- US20210180158A1. Zhou, N. "Ni-based superalloy powder for additive manufacturing and an article made therefrom." Patent (CRS Holdings/Carpenter Technology), 2021.

---

## 4. ATI 1700 by ATI Specialty Metals

### 4.1 Overview

**ATI 1700™** is a novel high-performance nickel-based superalloy developed by **ATI Specialty Materials** (Allegheny Technologies Incorporated) specifically for additive manufacturing. The alloy is being matured under the **America Makes PADAM** (Powder Alloy Development for Additive Manufacturing) initiative, a $6 million program funded by the **Air Force Research Laboratory (AFRL)**.

### 4.2 PADAM Program Details

- **Program**: America Makes PADAM — managed by the National Center for Defense Manufacturing and Machining (NCDMM)
- **Funding**: $6 million total, AFRL-funded
- **Project title**: "Accelerated Maturation of Advanced High-Performance Ni-Based Superalloy ATI-1700 for Additively Manufactured Extreme Environment Components"
- **Lead organization**: Boeing
- **Collaborators**: ATI Specialty Metals, Quintus Technologies, RPM Innovations
- **Objective**: Develop, qualify, and deploy ATI 1700 as a robust solution for demanding AM applications in aerospace and defense

### 4.3 Alloy Characteristics

- **AM compatibility**: Designed for both LPBF and directed energy deposition (DED)
- **Key properties**: High-temperature strength, creep resistance, environmental durability
- **Target applications**: Extreme-environment aerospace and defense components (hypersonic, propulsion)
- **Powder production**: ATI Specialty Metals provides gas-atomized powder optimized for AM (controlled particle size, chemistry, and sphericity)

**Note (Edison Scientific confirmation):** No published peer-reviewed literature exists on an alloy specifically designated "ATI 1700" through early 2026. This is consistent with the alloy being matured under the classified PADAM program.

### 4.3.1 ATI 718Plus Context

ATI's broader AM superalloy capability is demonstrated by **ATI 718Plus**, which provides context for their alloy design philosophy:

| Element | wt% |
|---------|-----|
| Ni | Balance |
| Cr | 17–21 |
| Fe | 8–10 |
| Co | 8–10 |
| Nb | 5.2–5.8 |
| Ti | 0.5–1 |
| Al | 1.2–1.7 |
| Mo | 2.5–3.1 |
| W | 0.8–1.4 |

- **γ' fraction**: ~21% (vs. ~4% in Alloy 718)
- **Service temp**: Up to 704°C (+55°C vs. Alloy 718)
- **Key design shift**: From metastable γ'' (Ni₃Nb) in 718 to stable γ' (Ni₃[Al,Ti,Nb]) in 718Plus

### 4.4 ATI Specialty Metals Capabilities

ATI is a primary developer and atomizer of specialty metal powders for AM, with capabilities spanning:
- Alloy design and atomization
- Powder qualification (chemistry, particle size distribution, flowability)
- Near-net-shape hot isostatic pressing (HIP)
- Powder recycling and reuse protocols

### 4.5 Key References

- "Winners of America Makes' Latest $6M Materials Project Announced." 3D Printing Industry (2023).
- "America Makes Announces Winners of Powder Alloy Development for Additive Manufacturing (PADAM) Project Totaling $6M." [americamakes.us](https://www.americamakes.us) (2023).
- "Additive Manufacturing of a Novel Nickel-Based Superalloy for High Temperature Applications." TMS 2024. [programmaster.org](https://www.programmaster.org)
- ATI Specialty Materials powder metals capabilities. [atimaterials.com](https://www.atimaterials.com/specialtymaterials/Pages/powder-metals.aspx)

---

## 5. NASA GRX-810

### 5.1 Overview

**GRX-810** is an oxide-dispersion strengthened (ODS) superalloy developed by **Dr. Tim Smith** and colleagues at **NASA Glenn Research Center**. It represents a breakthrough in combining ODS metallurgy with additive manufacturing, published in a landmark *Nature* paper in 2023. GRX-810 has been licensed to multiple U.S. companies for commercial production.

### 5.2 Alloy Composition

GRX-810 is a **medium-entropy alloy** based on the Ni-Co-Cr system. Precise nominal composition (wt%) from Smith et al. (2023, *Nature*):

**Ni-32Co-30Cr-3W-1.5Re-0.8Nb-0.3Ti-0.3Al-0.055C**, with <1 wt% nano Y₂O₃

| Element | wt% | Role |
|---------|-----|------|
| Ni | Balance (~33) | Matrix |
| Co | 32 | Solid solution strengthening, phase stability |
| Cr | 30 | Oxidation/hot corrosion resistance |
| W | 3.0 | Solid solution strengthening |
| Re | 1.5 | Creep resistance |
| Nb | 0.8 | Carbide formation |
| Al | 0.3 | Minor γ' former |
| Ti | 0.3 | Minor γ' former |
| C | 0.055 | Carbide strengthening |
| Y₂O₃ | 0.4–1.0 | Oxide dispersion strengthening |

**Solidus**: 1357°C

### 5.3 Strengthening Mechanisms

GRX-810 uses a fundamentally different strengthening approach than traditional γ'-strengthened superalloys:

- **Oxide dispersion strengthening (ODS)**: Uniformly dispersed nano-scale Y₂O₃ (yttria) particles provide extraordinary creep resistance by pinning dislocations and grain boundaries at extreme temperatures
- **Trigonal Y₂O₃ discovery** (Smith et al. 2025, *Nature Communications*, doi:10.1038/s41467-025-67687-4): Y₂O₃ particles adopt a **type-A trigonal crystal structure (space group P-3m1)** — the first observation of trigonal Y₂O₃ stable at ambient conditions in an NiCoCr-based ODS alloy. These are significantly finer with higher number density vs. cubic Y₂O₃ in other ODS alloys. Hypothesized to form during rapid LPBF solidification; quenching prevents reversion to stable cubic form. Provides ~2 orders of magnitude creep life improvement vs. non-ODS powder.
- **Solid solution strengthening**: W and Re provide additional matrix strengthening
- **Medium-entropy matrix**: The near-equimolar Ni-Co-Cr base provides inherent lattice distortion and sluggish diffusion
- **Nb/Ti-rich MC carbides**: At grain boundaries, provide additional dispersion strengthening
- **No ordered γ'**: Atomic-resolution characterization confirms no γ' phase and no local elemental ordering in the matrix
- **Novel processing**: Resonant acoustic mixing coats metal powder particles with nano-oxide particles before AM processing, ensuring uniform dispersion without traditional mechanical alloying

### 5.4 Mechanical Properties

**Performance at 1093°C (2000°F) compared to conventional AM superalloys:**

| Property | GRX-810 vs. Conventional |
|----------|-------------------------|
| Strength | ~2× stronger than IN718/IN625 at 1093°C |
| Creep rupture life | >1,000× longer |
| Oxidation resistance | ~2× better |
| Part lifespan | Up to 2,500× longer |

**Specific tensile values at 1093°C** (Smith et al. 2023):

| Condition | Tensile Strength (MPa) | Yield Strength (MPa) | Elongation (%) |
|-----------|----------------------|---------------------|----------------|
| As-built | ~128.9 | ~127.6 | ~22 |
| HIPed | ~119.3 | — | ~32 |

- Outperforms wrought alloys above ~850°C; surpasses single-crystal CMSX-4 above 1200°C
- Tensile testing extended to **1316°C** (97% of solidus)

**Creep data at 1093°C** (Smith et al. 2025, time to 1% creep strain):

| Alloy / Condition | Stress (MPa) | Time to 1% Creep (hours) |
|-------------------|-------------|-------------------------|
| GRX-810 as-built | 20 | 2,804 |
| GRX-810 HIP | 20 | 2,122 |
| GRX-810 CG (M280) | 21 | ~5,000 |
| NiCoCr (no ODS) | 20 | 0.35 |
| AM IN718 | 20 | 2.2 |
| AM IN625 | 20 | 10 |
| Wrought Haynes 230 | 20 | 5 |
| C-103 (refractory) | 20 | 1,170 |

At higher stresses (41 MPa): CG ~1,800 h vs. FG ~180 h; at 62 MPa both fail at ~10 h.

**Oxidation at 1100–1300°C:**
- At 1300°C (1-hour cyclic tests): Oxide layer 10–20 µm, no porosity/incipient melting
- Nano Y₂O₃ favors Cr₂O₃ formation and improves scale adhesion
- IN 718 exhibits runaway oxidation by 3rd cycle at 1300°C; GRX-810 maintains protective scale

**Aqueous corrosion** (Omoniyi et al. 2025, *Materials*, doi:10.3390/ma18143252, first dedicated study):
- As-built in 3.5 wt% NaCl: Ecorr = 187 mV, Icorr = 1.8 µA/cm²
- HIPed: Ecorr = −406 mV, Icorr = 11 µA/cm²
- As-built superior due to finer grain structure (~40 µm vs. ~193 µm after HIP) enabling faster repassivation

### 5.5 AM Processing

- **Primary process**: Laser powder bed fusion (L-PBF)
- **Powder preparation**: Resonant acoustic mixing of NiCoCr alloy powder with nano-Y₂O₃; scale-up from ~1 kg/hr to **18 kg/hr** throughput
- **EOS M280 parameters**: 270 W laser power, 1000 mm/s scan speed, 75 µm hatch spacing (energy density ~70–90 J/mm³)
- **Grain sizes**: Fine-grained (M100) ~34–39 µm; coarse-grained (M280) ~45–59 µm
- **HIP**: 1185°C/152 MPa; ODS prevents recrystallization during HIP
- **Platform progression**: M100 → M280/M290 → M400
- **Microstructure**: Refined grains with uniformly distributed nano-oxide particles
- **Powder recycling**: Properties maintained with recycled powder — key for sustainable manufacturing

### 5.6 Technology Transfer and Commercialization

NASA has licensed GRX-810 to multiple U.S. companies:
- **Elementum 3D** (commercializing as GRX-810)
- **Carpenter Technology Corporation** (PowderRange GRX-810 ODS)
- **Linde Advanced Material Technologies**
- **Powder Alloy Corporation**
- **3D Systems** (GRX-810(A) for DMP platform)

**TRL advancement**: From TRL 3 to **TRL 5** based on hot-fire testing (Gradl et al. 2024):
- **Cumulative hot-fire**: >3,117 seconds across LOX/LCH₄ and LOX/LH₂ at 37–57 bar
- **Sustained temperatures**: Average >820°C, local >1080°C
- **Injector performance**: 84 starts and 2,228 seconds (LOX/LCH₄); comparable Inconel injectors eroded after ~8–10 starts
- **Components demonstrated**: Pentad injectors, channel-cooled nozzles, turbine blisks, inducers
- **NASA programs**: ORCA, STMD Game Changing Program, TTT, SLS Liquid Engine Office
- **Nuclear applications**: Also evaluated for advanced nuclear reactor applications (McMurtrey et al. 2023)

### 5.7 Key References

- Smith, T.M. et al. "A 3D printable alloy designed for extreme environments." *Nature* 617, 513–518 (2023). doi:10.1038/s41586-023-05894-z *(224 citations)*
- Smith, T.M. et al. "The mechanisms underlying the enhanced high-temperature properties of GRX-810." *Nature Communications* (2025). doi:10.1038/s41467-025-67687-4 *(trigonal Y₂O₃ discovery)*
- Gradl, P. et al. "Extreme temperature additively manufactured GRX-810 alloy development and hot-fire testing for liquid rocket engines." *AIAA SCITECH 2024 Forum* (2024). doi:10.2514/6.2024-0997 *(11 citations)*
- Omoniyi, P. et al. "Corrosion behavior of additively manufactured GRX-810 alloy in 3.5 wt.% NaCl." *Materials*, 18:3252 (2025). doi:10.3390/ma18143252 *(first aqueous corrosion study)*
- US20200399744A1. Smith, T.M. "Additively manufactured oxide dispersion strengthened medium entropy alloys." Patent (NASA), 2020.
- NASA Glenn Research Center GRX-810 data sheets ([ntrs.nasa.gov](https://ntrs.nasa.gov))
- Carpenter Technology PowderRange GRX-810 ODS datasheet ([carpentertechnology.com](https://www.carpentertechnology.com))
- Elementum 3D GRX-810 product data sheet ([elementum3d.com](https://elementum3d.com))

---

## 6. Key Strengthening Mechanisms in LPBF Superalloys

### 6.1 Gamma Prime (γ') Quantity

The γ' phase (Ni₃(Al,Ti)) is the primary strengthening mechanism in most nickel superalloys. In the LPBF context:

- **Volume fraction vs. printability tradeoff**: Higher γ' fractions (>50%) provide superior creep resistance and high-temperature strength, but increase susceptibility to solidification and strain-age cracking during LPBF
- **Printability window**: Alloys with combined (Al + Ti) content below ~4.5 wt% are generally considered printable; above this, cracking risk increases significantly
- **Cracking indices**: Compositional indices such as the Msac index, defined here as `Msac = W_Al + 0.5W_Ti + 0.3W_Nb + 0.15W_Ta`, help predict printability; in this expression, `W_Al`, `W_Ti`, `W_Nb`, and `W_Ta` are the alloy contents of Al, Ti, Nb, and Ta expressed in **weight percent (wt%)**, not atomic fraction. See, for example, Wu et al., *Advances in crack susceptibility assessment for LPBF nickel superalloys*.
- **Optimization strategies**: New alloys (ABD-900AM, GammaPrint-1100) use computational design to find compositions that maximize γ' while remaining in the printable regime
- **ABD framework constraints**: Freezing range ≤ 280 K (Scheil); strain-age cracking index ≤ 3–4 wt%; >10⁷ trial compositions screened (Tang et al. 2021)
- **Defect comparison**: CM247LC crack density ~1.3 mm/mm² vs. ABD-850AM ~0.01 mm/mm² (Ghoussoub et al. 2022)
- **Lattice misfit engineering**: Positive misfit (+0.209 to +0.294%) shown to improve AM crack resistance vs. CM247LC negative misfit (−0.035%)

| Alloy | Approximate γ' Fraction | Max Service Temp | Printability |
|-------|------------------------|------------------|--------------|
| IN718 | ~15–20% | ~700°C | Excellent |
| ABD-900AM | ~35% | ~900°C | Excellent |
| GammaPrint-1100 | ~55–60% | >900°C | Good (designed) |
| A115 (GE) | Not disclosed | 780–880°C | Designed for LPBF |
| GRX-810 | Minimal (ODS-based) | >1093°C | Excellent |

### 6.2 Gamma Prime Solvus Temperature

The γ' solvus defines the temperature above which γ' precipitates dissolve into the matrix:

- **Service temperature ceiling**: The solvus effectively sets the maximum useful service temperature — the alloy loses precipitation strengthening above this point
- **Heat treatment windows**: Post-LPBF heat treatments (solution + aging) must be carefully designed relative to the solvus:
  - **Sub-solvus**: Preserves some grain structure; may yield incomplete dissolution
  - **Super-solvus**: Fully dissolves γ' for re-precipitation during controlled cooling; can cause excessive grain growth
  - **Near-solvus**: Optimal for many AM alloys — dissolves most γ' while limiting grain coarsening
- **Bimodal precipitate distribution**: Controlled cooling from near-solvus produces primary + secondary γ' populations that optimize creep and fatigue properties
- **AM-specific considerations**: The as-built LPBF microstructure contains fine, non-equilibrium γ' that differs from cast/wrought starting conditions, requiring modified heat treatment protocols

### 6.3 Solid Solution Strengthening

Refractory elements (W, Mo, Re, Ta, Cr) provide matrix strengthening in both γ and γ' phases:

- **W and Mo**: Partition to the γ matrix; increase anti-phase boundary energy; slow diffusion
- **Re**: Most potent solid solution strengthener (effectiveness ranking: Re > W > Mo > Ta in single-crystal Ni superalloys; Gaag et al. 2021, *Metals* 11:1707); 1.5 wt% in GRX-810 provides significant creep resistance; expensive and supply-constrained
- **Ta**: Partitions to γ'; increases γ' solvus; provides solid solution + precipitation strengthening
- **Cr**: Essential for oxidation/corrosion resistance; can destabilize γ' at high concentrations (formation of σ, μ phases)
- **LPBF-specific effects**: Rapid solidification in LPBF creates supersaturated solid solutions with higher solute content than equilibrium, potentially enhancing as-built strength but requiring careful post-processing

### 6.4 Hot Corrosion and Oxidation Resistance

- **Cr content**: Primary driver of oxidation/hot corrosion resistance; alloys targeting combustor environments (like A115) require high Cr levels
- **Al content**: Forms protective Al₂O₃ scales at higher temperatures; complementary to Cr₂O₃ protection; requires >9–11.5 at% for continuous alumina (Ghoussoub et al. 2023)
- **AM vs. conventional**: LPBF microstructures can show different oxidation behavior due to:
  - Finer grain structure (more grain boundary diffusion paths)
  - Residual porosity acting as oxidation initiation sites
  - Different element segregation patterns
  - Dislocation networks from rapid solidification
- **Environmental barrier coatings**: Compatibility with protective coatings (thermal barrier coatings, environmental barrier coatings) is critical for hot-section components

### 6.5 Recrystallization in Post-Processing

- **Driving force**: High dislocation density and residual stresses from LPBF provide strong driving force for recrystallization during heat treatment
- **Impact on properties**: Controlled recrystallization can improve fatigue life by eliminating columnar grain structures; uncontrolled recrystallization can create property scatter
- **Large builds**: 500 mm+ build platforms (as used by GE) create spatially varying thermal histories, leading to heterogeneous recrystallization behavior
- **Optimization**: Heat treatment ramp rates, hold temperatures, and cooling rates must be tailored to each alloy and part geometry

### 6.6 Cooling Rate Sensitivity

- **LPBF cooling rates**: 10⁴–10⁶ K/s — far higher than casting (1–100 K/s)
- **Spatial variation**: In large-format LPBF (500 mm+ platforms), the bottom of a build experiences different thermal cycling than the top, affecting:
  - γ' precipitation kinetics
  - Residual stress distribution
  - Recrystallization tendency
  - Microchemical segregation
- **Implications**: Alloys must be robust to a range of cooling rates, or builds must use adaptive process parameters

### 6.7 Age Hardening Cycle Optimization

- **Temperature sensitivity**: AM microstructures respond differently to aging than cast/wrought due to non-equilibrium starting conditions
- **Time sensitivity**: Over-aging can coarsen γ' precipitates, reducing strength; under-aging leaves strength on the table
- **Multi-step aging**: Many AM superalloys use two-step aging (high-temperature + low-temperature) to develop bimodal γ' distributions
- **Alloy-specific windows**: Each new AM alloy requires bespoke aging optimization — transferring protocols from cast/wrought counterparts is often inadequate

---

## 7. Competitive Landscape Summary

| Alloy | Developer | Service Temp | γ' Fraction | Strengthening | AM Process | TRL |
|-------|-----------|-------------|-------------|---------------|-----------|-----|
| A94 | GE Aerospace | 650–780°C | Medium-High | γ' precipitation | LPBF (500mm) | Mid |
| A115 | GE Aerospace | 780–880°C | High | γ' precipitation | LPBF (500mm) | Mid |
| ABD-900AM | Alloyed/Aubert & Duval | ~900°C | ~35% | γ' precipitation | LPBF | High |
| ABD-1000AM | Alloyed/Aubert & Duval | >1000°C | Higher | γ' precipitation | LPBF | Mid |
| GammaPrint-1100 | Carpenter/ORNL | >900°C | 55–60% | γ' precipitation | LPBF | Mid-High |
| ATI 1700 | ATI/Boeing | High | Not disclosed | γ' precipitation | LPBF + DED | Mid |
| GRX-810 | NASA Glenn/Licensees | >1093°C | Minimal | ODS (Y₂O₃) + SSS | LPBF | TRL 5 |
| IN718 (baseline) | Multiple | ~700°C | 15–20% | γ'/γ'' precipitation | LPBF | High |

**Key observations:**
1. The field is rapidly moving beyond IN718 toward alloys with higher service temperatures
2. Two distinct strengthening strategies: traditional γ' precipitation (A94, A115, ABD, GammaPrint, ATI 1700) vs. ODS (GRX-810)
3. Computational alloy design (CALPHAD, ICME, ABD platform) is enabling systematic optimization of printability–performance tradeoffs
4. Large-format LPBF (500 mm+ platforms) introduces new challenges in thermal management and property uniformity
5. Government programs (DOE AMMTO, AFRL/America Makes PADAM, NASA tech transfer) are major drivers of development
6. Compatibility with downstream processes (brazing, welding, coatings) is a critical but less-studied consideration

---

## 8. Key Research Groups and Institutions

| Group/Institution | Focus Area | Key Alloys |
|-------------------|-----------|-----------|
| GE Aerospace Research (Laura Dial) | A94, A115, LPBF scale-up | A94, A115 |
| Alloyed / University of Oxford (Roger Reed) | ABD platform, computational design | ABD-900AM, ABD-1000AM |
| Carpenter Technology / ORNL (M.M. Kirka) | GammaPrint, DOE-funded development | GammaPrint-1100, GammaPrint-700 |
| ATI Specialty Metals / Boeing | PADAM, powder atomization | ATI 1700 |
| NASA Glenn (Tim Smith) | ODS alloys, resonant acoustic mixing | GRX-810 |
| Ohio State University | ODS characterization, electron microscopy | GRX-810 collaboration |
| Aubert & Duval | ABD-900AM/1000AM commercialization | ABD family |
| Elementum 3D | GRX-810 commercialization | GRX-810 |

---

*Edison Scientific LITERATURE_HIGH queries were submitted for all alloys and all completed successfully. Task IDs and results: GE A94/A115 (1a8f8a4e, 19K chars — confirmed proprietary designations); ABD-900AM (3e830fe0, 52K chars, 38 citations); GammaPrint (b5b9e801, 40K chars); ATI 1700 (afb26a54, 10K chars — confirmed no publications); GRX-810 (0224546d, 42K chars); strengthening mechanisms (590bbdd9, 57K chars). Total: ~220K chars of peer-reviewed literature analysis with 100+ unique citations. Web search used for supplementary cross-referencing with conference proceedings (TMS 2026, Superalloys 2024), journal articles (Nature 2023, Acta Materialia, ASME J. Gas Turbines Power), government databases (OSTI, NTRS), manufacturer datasheets, and patent filings.*
