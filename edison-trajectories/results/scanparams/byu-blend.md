# BYU AA1100 + Si + AlSi10Mg blend (Al 75.56 / Si 24.30 / Mg 0.14 wt%)

_Edison task_id: `fe1fee02-ba7a-4a46-9da8-529bc13169cc`  
_status: success_

---

# LPBF Scan Parameters and Printability-Map Grid-Search Plan for Al-75.56 / Si-24.30 / Mg-0.14 wt%

## 1. Single-Point Reference Parameters

The following table provides a complete recommended starting point for a Thermo-Calc AM Module steady-state Single-Point calculation. Every field from the AM Module Conditions menu is addressed, with explicit notation of deviations from Thermo-Calc defaults and literature justification for each change.

| Parameter name | Recommended value | Default value | Changed from default | Justification with literature reference |
|---|---:|---:|:---:|---|
| Gas pressure | 1.0e5 Pa | 1.0e5 Pa | No | Leave at Thermo-Calc default; hypereutectic Al-Si LPBF studies cited here were run in Ar with low O\(_2\), but no composition-specific pressure deviation is established for Al-24.3Si, so default atmospheric pressure is the least-assumptive steady-state starting point (risse2023microstructureandmechanical pages 2-4). |
| Base-plate temperature | 30 °C | 30 °C | No | Risse et al. printed hypereutectic AlSi50/70 on an unheated Al base plate and obtained crack-free AlSi50 over 24–97 J/mm\(^3\); no clear evidence supports mandatory preheat for this Si-rich alloy, unlike some crack-prone wrought Al systems (risse2023microstructureandmechanical pages 6-8, risse2023microstructureandmechanical pages 2-4). |
| Ambient temperature | 23 °C | 23 °C | No | No composition-specific evidence justifies changing ambient temperature; keep Thermo-Calc default for the preliminary steady-state run (risse2023microstructureandmechanical pages 2-4). |
| Fluid-flow / Marangoni | On | On | No | Keep default because melt-pool convection materially affects LPBF melt-pool shape and regime transitions; no literature suggests suppressing Marangoni flow for hypereutectic Al-Si (depond2020detectingkeyholeporosity pages 19-22, zhao2022lasermeltingmodes pages 15-17). |
| Separate powder density | 80% of solid | 80% of solid | No | Keep default; powder-bed absorptance is substantially higher than bare plate and this default is consistent with standard LPBF powder-bed modeling assumptions for Al alloys (reed2024timeresolvedabsorptancein pages 83-89, trapp2017insituabsorptivity pages 1-2). |
| Height | 2.0 mm | 2.0 mm | No | Leave default; sufficient for preliminary steady-state melt-pool calculations and consistent with AM Module guidance. |
| Mesh | Coarse | Coarse | No | Leave default for preliminary deliverable; no composition-specific need for finer mesh at this stage. |
| Heat source type | Gaussian | Gaussian | No | Use Gaussian as requested unless clear ring-mode motivation exists; no hypereutectic Al-Si evidence here requires core-ring for the first pass (risse2023microstructureandmechanical pages 2-4). |
| Laser power | 275 W | 200 W | Yes | Raise above default because the closest hypereutectic analogue (AlSi50 on an Aconity system) was optimized at 350 W with 50 µm layers and 120 µm hatch, while AlSi10Mg optima are ~175–200 W at thinner 30 µm layers. A mid-range 275 W is a conservative bridge for Al-24.3Si on an Aconity MIDI and remains inside the 50–400 W machine envelope (risse2023microstructureandmechanical pages 2-4, kempen2011processoptimizationand pages 8-12, read2015selectivelasermelting pages 4-5, read2015selectivelasermelting pages 2-4). |
| Absorptivity mode | Calculated | Calculated | No | Use Thermo-Calc calculated mode per constraint; direct constant override is not well-supported for this exact composition. However, note that Al-Si absorptivity differs from AlSi10Mg calibration, so this is a pragmatic first pass rather than a validated truth model (reed2024timeresolvedabsorptancein pages 83-89, indhu2018overviewoflaser pages 12-16, gunenthiram2018experimentalanalysisof pages 13-19). |
| Absorptivity prefactor | 1.0 | 1.0 | No | Keep default because no exact literature-calibrated constant exists for Al-24.3Si powder bed at 1064–1080 nm. AlSi10Mg powder absorptance is high (~0.74–0.77) while bulk/bare Al-Si can be much lower, so a prefactor change would be speculative at this stage (reed2024timeresolvedabsorptancein pages 83-89, indhu2018overviewoflaser pages 12-16, reed2024timeresolvedabsorptancein pages 27-31). |
| Laser wavelength | 1064 nm | 1064 nm | No | Matches Aconity MIDI near-IR fiber laser and literature Aconity hypereutectic study at 1080 nm; no reason to deviate (risse2023microstructureandmechanical pages 2-4). |
| Beam radius | 45 µm | 40 µm | Yes | Increase modestly to reflect typical Aconity MIDI 40–80 µm optics and to better align with the 72 µm spot diameter used by Risse et al. (≈36 µm radius) while avoiding an overly tight beam at elevated power; 45 µm is a conservative, machine-representative start (risse2023microstructureandmechanical pages 2-4). |
| Keyhole model | On | On | No | Keep on because Al alloys can cross into transition/keyhole behavior over the intended P–v map, and absorptivity/melt-pool depth change strongly across that threshold (depond2020detectingkeyholeporosity pages 19-22, huang2022keyholefluctuationand pages 2-4, reed2024timeresolvedabsorptancein pages 83-89). |
| Beam-quality factor M² | 1.0 | 1.0 | No | Leave default; no composition-specific evidence supports altering M². |
| Scanning speed | 1400 mm/s | 1000 mm/s | Yes | Increase from default because the closest hypereutectic Aconity study found lowest porosity for AlSi50 around 1400–2000 mm/s at 350 W, while too-low speeds in AlSi10Mg promote excess energy input/distortion and too-high speeds risk poor wetting. 1400 mm/s is an evidence-based center-point for hypereutectic exploration (risse2023microstructureandmechanical pages 2-4, risse2023microstructureandmechanical pages 4-6, kempen2011processoptimizationand pages 3-8). |
| Layer thickness | 30 µm | 40 µm | Yes | Change to 30 µm because Al-alloy LPBF commonly uses 30 µm, and thinner layers are prudent for this hypereutectic blend to secure melt depth >1–1.5× layer thickness while refining primary Si and reducing lack-of-fusion risk (read2015selectivelasermelting pages 2-4, wang2024areviewon pages 5-7, risse2023microstructureandmechanical pages 1-2). |
| Radiation emissivity | 0.8 | 0.8 | No | Keep default; no composition-specific emissivity override is well-supported here. |
| Convective HTC | 20 W/m²/K | 20 W/m²/K | No | Keep default; no literature-backed reason to deviate for this alloy in a preliminary steady-state run. |
| Evaporation | On | On | No | Keep on because even small Mg contents can evaporate in Al-Si LPBF and evaporation effects are relevant near upper-energy conditions; default is physically appropriate (wang2024areviewon pages 5-7). |
| Calculation type | Single Point | Single Point | No | Recommended starting condition for the steady-state reference run before broader Grid sweeps. |


*Table: This table gives a literature-grounded starting parameter set for a Thermo-Calc AM Module steady-state run for the nominal Al-75.56Si24.30Mg0.14 wt% blend, marking which settings remain at default versus which are adjusted to better match hypereutectic Al-Si LPBF evidence and Aconity-representative operation.*

**Summary of deviations from default:**

Three parameters are changed from the Thermo-Calc defaults:

1. **Laser power: 275 W (default 200 W).** The closest published hypereutectic analogue is AlSi50 processed on an Aconity mini PBF-LB/M system at 350 W with 50 µm layers and 120 µm hatch (risse2023microstructureandmechanical pages 2-4). AlSi10Mg optima cluster around 175–200 W at 30 µm layers (kempen2011processoptimizationand pages 8-12, read2015selectivelasermelting pages 4-5). Since Al-24.3Si lies between AlSi10Mg and AlSi50 in silicon content (and thus in thermal conductivity and melt-pool behavior), 275 W represents a reasonable interpolation within the Aconity MIDI envelope (50–400 W).

2. **Scanning speed: 1400 mm/s (default 1000 mm/s).** Risse et al. found porosity minima for AlSi50 between 1400 and 2000 mm/s at 350 W; below 1000 mm/s, excessive energy input causes distortion and balling in Al-Si alloys (risse2023microstructureandmechanical pages 2-4, risse2023microstructureandmechanical pages 4-6, kempen2011processoptimizationand pages 3-8). This is well within the Aconity MIDI range of ~100–3000 mm/s.

3. **Layer thickness: 30 µm (default 40 µm).** Al-alloy LPBF commonly uses 30 µm layers (read2015selectivelasermelting pages 2-4). For this hypereutectic blend—especially one prepared from mixed elemental/pre-alloyed feedstock—thinner layers help ensure full remelting and reduce lack-of-fusion risk while refining primary Si phases (wang2024areviewon pages 5-7, risse2023microstructureandmechanical pages 1-2).

**Beam radius** is set at 45 µm (vs. default 40 µm) to better represent the Aconity MIDI optics, where Risse et al. used a 72 µm spot diameter (~36 µm radius) on a similar Aconity platform (risse2023microstructureandmechanical pages 2-4). This is a minor deviation that should be noted to Thermo-Calc's account manager.

---

## 2. Grid-Search Plan for a P–v Printability Map

**Axes and bounds:**

| Parameter | Min | Max | Resolution | Rationale |
|-----------|-----|-----|------------|-----------|
| Laser power (P) | 100 W | 400 W | 7 levels (100, 150, 200, 250, 275, 325, 400 W) | Spans the full Aconity MIDI range. AlSi10Mg optima lie near 175–200 W (kempen2011processoptimizationand pages 8-12, read2015selectivelasermelting pages 4-5); hypereutectic AlSi50 was run at 350 W (risse2023microstructureandmechanical pages 2-4). |
| Scan speed (v) | 400 mm/s | 2400 mm/s | 9 levels (400, 600, 800, 1000, 1200, 1400, 1600, 2000, 2400 mm/s) | Covers the full range explored by Risse et al. for AlSi50 (1000–2400 mm/s) and extends to lower speeds to capture the conduction-to-keyhole transition (risse2023microstructureandmechanical pages 2-4, risse2023microstructureandmechanical pages 4-6). |

**Grid size:** 7 × 9 = **63 points**. This is computationally tractable for the AM Module Grid mode and provides adequate resolution to resolve the conduction–transition–keyhole boundaries.

**Held-constant parameters:**

- **Layer thickness: 30 µm** (fixed across sweep)
- **Hatch spacing: 100 µm** (interpolated between 105 µm for AlSi10Mg (kempen2011processoptimizationand pages 8-12) and 120 µm for AlSi50 (risse2023microstructureandmechanical pages 2-4); a round number that gives ~60% overlap with a ~250 µm expected track width at mid-range conditions)
- **Beam radius: 45 µm** (fixed)
- All other parameters as in the single-point table above

**Volumetric energy density (VED) coverage:** At these bounds, VED = P/(v × h × t) ranges from ~14 J/mm³ (400 W, 2400 mm/s corner is actually ~56 J/mm³; 100 W, 2400 mm/s gives ~14 J/mm³) to ~333 J/mm³ (400 W, 400 mm/s). This brackets the 24–97 J/mm³ range identified as crack-free for AlSi50 (risse2023microstructureandmechanical pages 4-6, risse2023microstructureandmechanical pages 6-8) and extends into both lack-of-fusion and keyhole territories.

**Third parameter note:** If a secondary grid is desired, **base-plate preheat** (30 °C vs. 150 °C) would be the most informative third axis for this composition, as moderate preheating may reduce thermal gradients and primary-Si coarsening. However, since Risse et al. achieved crack-free AlSi50 without preheating (risse2023microstructureandmechanical pages 6-8), this should remain a secondary investigation and not complicate the primary P–v map.

---

## 3. Expected LPBF Windows / Regimes

Based on the literature evidence for hypereutectic Al-Si and Al-alloy melting-mode physics, the following regime predictions are offered for the 7 × 9 P–v grid:

**Lack-of-fusion region:** Expected at low power / high speed (P ≤ 150 W, v ≥ 1600 mm/s), corresponding to VED < ~30 J/mm³. Melt-pool depth will be insufficient to penetrate the 30 µm powder layer, producing inter-layer unbonded regions. This composition's high thermal conductivity (Al-Si ~150–170 W/m·K) exacerbates heat dissipation and pushes the lack-of-fusion boundary to higher VED than for steels (wang2024areviewon pages 5-7).

**Conduction-mode region:** Expected at moderate conditions — roughly P = 150–250 W, v = 800–1600 mm/s (VED ~30–80 J/mm³). This is the target processing window. Shallow, stable melt pools with depth/width < 0.5 are anticipated. Primary Si refinement should be strong here due to cooling rates of 10⁴–10⁶ K/s (wang2024areviewon pages 5-7, risse2023microstructureandmechanical pages 1-2).

**Transition region:** Expected at P = 250–350 W, v = 600–1200 mm/s (VED ~70–150 J/mm³). Sporadic keyhole formation will cause intermittent absorptivity jumps (depond2020detectingkeyholeporosity pages 19-22, reed2024timeresolvedabsorptancein pages 83-89). This regime is the most informative for the FLAIME BOFN surrogate, as it maps the boundary where process instabilities begin.

**Keyhole region:** Expected at high power / low speed (P ≥ 350 W, v ≤ 600 mm/s), corresponding to VED > ~150 J/mm³. Deep, unstable vapor depressions will form, trapping gas porosity. The normalized-enthalpy keyhole threshold for Al alloys is lower than for steels due to Al's lower melting enthalpy (~2.63 J/mm³ vs. ~6.26 J/mm³ for steel) and low bare-surface absorptivity (~0.15), meaning keyhole onset may be abrupt once the threshold power density is reached (huang2022keyholefluctuationand pages 2-4, gunenthiram2018experimentalanalysisof pages 13-19).

**Most informative region for BOFN surrogate:** The transition zone (P = 200–350 W, v = 800–1600 mm/s) is where small parameter perturbations produce the largest changes in melt-pool morphology and defect population. Dense sampling in this region (the center of the grid) will maximize the information gain for Bayesian optimization.

---

## 4. Composition-Specific Flags

### 4a. Absorptivity behavior relative to AlSi10Mg

The Thermo-Calc AM Module's absorptivity is calibrated against AlSi10Mg (prefactor 1.0). For this Al-24.3Si composition, several differences should be noted:

- **Powder-bed absorptance** for AlSi10Mg at ~1070 nm is ~0.74–0.77 in conduction mode, dropping to ~0.04–0.18 on bare/previously-melted surfaces (reed2024timeresolvedabsorptancein pages 83-89). The Si-rich powder blend will contain ~24 wt% elemental/alloyed Si particles. Crystalline Si is semi-transparent at 1064 nm at room temperature but becomes highly absorbing above ~500 °C as the bandgap narrows. This means early-stage laser coupling into the Si-rich powder bed may initially be *lower* than AlSi10Mg (which is fully metallic), but once heated, absorptivity may rise more steeply.
- **Recommendation:** Use Calculated mode with prefactor 1.0 for the first pass, but Thermo-Calc's account manager should flag that the model may underestimate the initial reflectivity of Si-rich powder and overestimate steady-state absorptivity. A sensitivity run with prefactor 0.8–1.2 is advisable (indhu2018overviewoflaser pages 12-16, reed2024timeresolvedabsorptancein pages 27-31, trapp2017insituabsorptivity pages 1-2).

### 4b. L1₂ vs. D0₂₃ phase handling

This composition contains no Zr, so L1₂-Al₃Zr / D0₂₃-Al₃Zr phase handling is **not applicable**. The relevant solidification phases are:

- **Primary Si** (diamond cubic): Nucleates first from the hypereutectic melt at ~780–850 °C (liquidus for Al-24Si is approximately 800–810 °C from the Al-Si binary phase diagram)
- **Al-Si eutectic** at 577 °C: α-Al + Si
- **Mg₂Si**: Minor, given only 0.14 wt% Mg

In the Scheil / AM-Module setup, ensure all equilibrium Si phases are active. No metastable phase suspension is required for this Zr-free composition.

### 4c. Hot-cracking / solidification-cracking susceptibility

Hypereutectic Al-Si alloys are generally **resistant to hot cracking** in LPBF. The narrow freezing range (liquidus ~810 °C to eutectic 577 °C, but the eutectic fraction is large) and the dominance of the eutectic reaction provide excellent crack healing. Risse et al. confirmed crack-free AlSi50 over the full 24–97 J/mm³ VED range tested (risse2023microstructureandmechanical pages 6-8, risse2023microstructureandmechanical pages 1-2). At 24.3 wt% Si, cracking susceptibility should be low, but primary Si particles can act as stress concentrators under high thermal gradients — hence the recommendation to avoid extremely high VED (> ~150 J/mm³).

### 4d. Feedstock-specific flags that affect scan parameters

- **Blended powder homogeneity:** The BYU feedstock is a tri-component blend (AA1100 wire-derived powder + Si powder + AlSi10Mg powder). Risse et al. showed that powder blends can produce comparable properties to pre-alloyed powders for hypereutectic Al-Si, but local composition inhomogeneity in the powder bed can cause melt-pool instabilities (risse2023microstructureandmechanical pages 1-2, risse2023microstructureandmechanical pages 2-4). The elemental Si powder particles are angular (non-spherical), which reduces flowability and packing density. The operator should expect slightly higher porosity at the extremes of the P–v map than pre-alloyed powder would produce.
- **Mg vapor loss:** At 0.14 wt% Mg, evaporative losses at high VED may effectively eliminate Mg from the solidified material. This does not change recommended scan parameters but should be tracked in the Thermo-Calc simulation (evaporation is left ON) (wang2024areviewon pages 5-7).
- **Si particle size mismatch:** If the Si powder fraction has a significantly different particle size distribution than the AlSi10Mg and AA1100 fractions, segregation during recoating is possible. This is a physical-build concern for the BYU operator rather than a simulation concern for Thermo-Calc's account manager.

---

## 5. Citations

1. **Risse et al. (2023)** — Microstructure and mechanical properties of hypereutectic Al-high Si alloys up to 70 wt.% Si-content produced from pre-alloyed and blended powder via laser powder bed fusion. *Materials*, 16, 657. DOI: [10.3390/ma16020657](https://doi.org/10.3390/ma16020657) (risse2023microstructureandmechanical pages 2-4, risse2023microstructureandmechanical pages 4-6, risse2023microstructureandmechanical pages 6-8, risse2023microstructureandmechanical pages 1-2, risse2023microstructureandmechanical pages 12-13)

2. **Kempen et al. (2011)** — Process optimization and microstructural analysis for selective laser melting of AlSi10Mg. DOI: [10.26153/tsw/15310](https://doi.org/10.26153/tsw/15310) (kempen2011processoptimizationand pages 8-12, kempen2011processoptimizationand pages 3-8)

3. **Read et al. (2015)** — Selective laser melting of AlSi10Mg alloy: Process optimisation and mechanical properties development. *Materials & Design*, 65, 417–424. DOI: [10.1016/j.matdes.2014.09.044](https://doi.org/10.1016/j.matdes.2014.09.044) (read2015selectivelasermelting pages 4-5, read2015selectivelasermelting pages 2-4)

4. **Yang et al. (2018)** — Porosity formation mechanisms and fatigue response in Al-Si-Mg alloys made by selective laser melting. *MSEA*, 712, 166–174. DOI: [10.1016/j.msea.2017.11.078](https://doi.org/10.1016/j.msea.2017.11.078) (yang2018porosityformationmechanisms pages 16-18)

5. **Wang et al. (2024)** — A Review on Traditional Processes and LPBF of Aluminum Alloy. *Materials*, 17, 2553. DOI: [10.3390/ma17112553](https://doi.org/10.3390/ma17112553) (wang2024areviewon pages 5-7)

6. **Reed (2024)** — Time-Resolved Absorptance in Laser-Powder Bed Fusion: Effect of Gaussian and Novel Beam Shapes. (reed2024timeresolvedabsorptancein pages 83-89, reed2024timeresolvedabsorptancein pages 27-31)

7. **Trapp et al. (2017)** — In situ absorptivity measurements of metallic powders during laser powder-bed fusion additive manufacturing. *Applied Materials Today*, 9, 341–349. DOI: [10.1016/j.apmt.2017.08.006](https://doi.org/10.1016/j.apmt.2017.08.006) (trapp2017insituabsorptivity pages 1-2)

8. **Indhu et al. (2018)** — Overview of Laser Absorptivity Measurement Techniques for Material Processing. *Lasers in Manufacturing and Materials Processing*, 5, 458–481. DOI: [10.1007/s40516-018-0075-1](https://doi.org/10.1007/s40516-018-0075-1) (indhu2018overviewoflaser pages 12-16)

9. **DePond et al. (2020)** — Detecting keyhole porosity and monitoring process signatures in additive manufacturing. (depond2020detectingkeyholeporosity pages 19-22)

10. **Huang et al. (2022)** — Keyhole fluctuation and pore formation mechanisms during laser powder bed fusion additive manufacturing. *Nature Communications*, 13. DOI: [10.1038/s41467-022-28694-x](https://doi.org/10.1038/s41467-022-28694-x) (huang2022keyholefluctuationand pages 2-4)

11. **Gunenthiram et al. (2018)** — Experimental analysis of spatter generation and melt-pool behavior during the powder bed laser beam melting process. *JMPT*, 251, 376–386. DOI: [10.1016/j.jmatprotec.2017.08.012](https://doi.org/10.1016/j.jmatprotec.2017.08.012) (gunenthiram2018experimentalanalysisof pages 13-19)

12. **Zhao et al. (2022)** — Laser melting modes in metal powder bed fusion additive manufacturing. *Reviews of Modern Physics*, 94. DOI: [10.1103/revmodphys.94.045002](https://doi.org/10.1103/revmodphys.94.045002) (zhao2022lasermeltingmodes pages 15-17)

13. **He (2021)** — Design and development of high strength aluminium materials for laser powder-bed fusion additive manufacturing. Dissertation, UNSW Sydney. DOI: [10.26190/unsworks/22600](https://doi.org/10.26190/unsworks/22600) (he2021designanddevelopment pages 30-35)

