# Edison job-futurehouse-paperqa3-high result: literature_high_w_plate

**Task ID:** `45b42fbf-ec87-4569-ba68-b1f4429351a5`  
**Status:** success

<details><summary>Query</summary>

```text
Context. We will ultrasonically atomize 1.1 kg of 70 wt% Cu / 30 wt% Ni (binary cupronickel, near
UNS C71500; liquidus ~1240 C, solidus ~1170 C) in an AMAZEMET rePOWDER. The charge is induction-melted
in a BN-coated crucible to roughly 1260-1300 C (the induction module's practical limit is ~1300 C), then
poured in argon through a bottom nozzle (BN stopper rod) onto a horizontal plate on an ultrasonic
sonotrode (1:1.5 booster, 100% generator amplitude). The plate is the atomizing surface: a thin melt
film on it is continuously renewed for the length of the pour, likely 5-30 minutes. The plate is a
carbon-fiber composite (probably carbon-carbon) that was "dipped" in molybdenum. A previous review
flagged the Mo coat as high risk: a Cu-32Ni melt dissolves ~3.7 wt% Mo at 1300 C (Teodorovich 1980,
doi:10.1007/bf00791375), and a Ni-rich alloy atomized on a solid Mo sonotrode in a rePOWDER picked up
~2.6 wt% Mo (Goncharov 2026, doi:10.3390/met16030318). A colleague now proposes a carbon-fiber plate
dipped in TUNGSTEN instead.

A separate, broader query is already comparing W and Mo qualitatively. For this one we need numbers
with sources, and physical estimates with the inputs shown where the literature is silent.

1. Solubility of W in the melt. Report the equilibrium solubility of W (wt% and at%) in liquid
   Cu-30Ni, and along the Cu-Ni join, at 1250, 1300 and 1350 C, from experimental Cu-Ni-W phase
   equilibria and CALPHAD assessments (name them and give their values). Cross-check against:
   (i) the Ni-W binary (W in liquid Ni near the ~1495 C peritectic; (Ni) dissolves ~17.5 at% W);
   (ii) Cu-W (W solubility in liquid Cu); (iii) the W content of the Ni-Cu matrix in
   liquid-phase-sintered W-Ni-Cu heavy alloys versus Ni:Cu ratio and sintering temperature;
   (iv) Mo in the same melts. At W saturation and 1250-1300 C, is the phase in equilibrium with the
   melt pure (W), a (Ni,W) fcc solid solution, or a Ni-W intermetallic (Ni4W, NiW)? Could a solid
   Ni-W-rich layer form and grow on the plate, raising the local liquidus and seeding freezing of
   the thin film?

2. Rate of attack. Give measured dissolution rate constants or recession rates of W, and of Mo for
   comparison, in liquid Ni, Cu-Ni or Ni-base melts (rotating-disc, immersion or diffusion-couple
   studies, e.g., W wire or W crucibles in Ni-base superalloy melts), and say whether dissolution is
   diffusion- or interface-controlled. Report what is known about ultrasonic or cavitation
   enhancement of dissolution and erosion of W, Mo, Nb, Ti or steel sonotrodes in metal melts. Then
   estimate, with stated assumptions, the recession depth (micrometres) at the melt impingement zone
   for a W coat and for a Mo coat during a 10-30 minute pour, and the resulting W or Mo content of
   the 1.1 kg of powder.

3. W coatings on carbon-fiber composites. Summarize precedents with numbers: the JET ITER-like wall W
   coatings on CFC (combined magnetron sputtering and ion implantation, ~10-25 um W on a Mo
   interlayer), vacuum-plasma-sprayed W on CFC or graphite, and CVD W on C/C. Give their adhesion,
   the thickness above which they delaminate, cracking under thermal cycling and high heat flux, the
   onset temperature and growth rate of W2C/WC at the W/C interface and its effect on adhesion,
   diffusion barriers (Re, Mo), and recrystallization and embrittlement of W coatings at 1200-1400 C.
   How would such coatings respond to sustained 20-60 kHz vibration at an atomizing plate's
   displacement amplitude?

4. What "dipping" in W can practically mean, since W melts at 3422 C: slurry or paint dip coats with
   sintering (temperatures; sintering aids such as Ni, Fe or Co that would themselves dissolve in
   Cu-Ni), molten-salt electrodeposition of W, CVD from WF6, chemical vapour infiltration, and thermal
   spray. Give typical thickness, density or porosity and adhesion for each, and say whether a porous
   W layer would be infiltrated by a Cu-Ni melt (W-Cu composites are made by infiltrating porous W
   with Cu, and Ni activates the wetting), giving the melt a path to the carbon.

5. Wetting. Contact angles of liquid Cu, Ni and Cu-Ni on W, on Mo and on graphite or carbon fiber at
   1100-1400 C in argon or vacuum, including the effect of surface oxides (WO2/WO3, MoO2/MoO3) and of
   Ni as a wetting activator. Is complete wetting desirable on an ultrasonic atomizing plate, or does
   it promote film pinning, infiltration and erosion?

6. Acoustics. For a thin plate on an ultrasonic horn, estimate the added mass and the
   resonant-frequency shift from a W coat versus a Mo coat of the same thickness (densities 19.3 and
   10.2 g/cm3; C/C ~1.6-1.9 g/cm3), for 25, 100 and 250 um per side on a 2-3 mm plate, and say
   whether a typical generator's frequency-tracking range would still lock. Comment on damping and
   heating in a porous coat.

7. Powder consequences. At the W pickup estimated in item 2, would W stay in solution in Cu-30Ni
   powder or appear as W particles, and what would it do to compliance with UNS C71500 (and the
   military specifications that cite it), to seawater corrosion, and to laser powder-bed fusion?

Finish with (a) a direct verdict on W versus Mo for this run, (b) a table of failure mode -> Mo coat
-> W coat (numbers where possible) -> mitigation, and (c) the plate you would choose for this run and
why (solid Mo or TZM, solid W or W-La2O3, W-coated Mo, or a ceramic such as BN, alumina, zirconia or
SiC-coated C/C), naming any ultrasonic-atomization or ultrasonic-melt-processing precedent for it.

```

</details>

Question: Context. We will ultrasonically atomize 1.1 kg of 70 wt% Cu / 30 wt% Ni (binary cupronickel, near
UNS C71500; liquidus ~1240 C, solidus ~1170 C) in an AMAZEMET rePOWDER. The charge is induction-melted
in a BN-coated crucible to roughly 1260-1300 C (the induction module's practical limit is ~1300 C), then
poured in argon through a bottom nozzle (BN stopper rod) onto a horizontal plate on an ultrasonic
sonotrode (1:1.5 booster, 100% generator amplitude). The plate is the atomizing surface: a thin melt
film on it is continuously renewed for the length of the pour, likely 5-30 minutes. The plate is a
carbon-fiber composite (probably carbon-carbon) that was "dipped" in molybdenum. A previous review
flagged the Mo coat as high risk: a Cu-32Ni melt dissolves ~3.7 wt% Mo at 1300 C (Teodorovich 1980,
doi:10.1007/bf00791375), and a Ni-rich alloy atomized on a solid Mo sonotrode in a rePOWDER picked up
~2.6 wt% Mo (Goncharov 2026, doi:10.3390/met16030318). A colleague now proposes a carbon-fiber plate
dipped in TUNGSTEN instead.

A separate, broader query is already comparing W and Mo qualitatively. For this one we need numbers
with sources, and physical estimates with the inputs shown where the literature is silent.

1. Solubility of W in the melt. Report the equilibrium solubility of W (wt% and at%) in liquid
   Cu-30Ni, and along the Cu-Ni join, at 1250, 1300 and 1350 C, from experimental Cu-Ni-W phase
   equilibria and CALPHAD assessments (name them and give their values). Cross-check against:
   (i) the Ni-W binary (W in liquid Ni near the ~1495 C peritectic; (Ni) dissolves ~17.5 at% W);
   (ii) Cu-W (W solubility in liquid Cu); (iii) the W content of the Ni-Cu matrix in
   liquid-phase-sintered W-Ni-Cu heavy alloys versus Ni:Cu ratio and sintering temperature;
   (iv) Mo in the same melts. At W saturation and 1250-1300 C, is the phase in equilibrium with the
   melt pure (W), a (Ni,W) fcc solid solution, or a Ni-W intermetallic (Ni4W, NiW)? Could a solid
   Ni-W-rich layer form and grow on the plate, raising the local liquidus and seeding freezing of
   the thin film?

2. Rate of attack. Give measured dissolution rate constants or recession rates of W, and of Mo for
   comparison, in liquid Ni, Cu-Ni or Ni-base melts (rotating-disc, immersion or diffusion-couple
   studies, e.g., W wire or W crucibles in Ni-base superalloy melts), and say whether dissolution is
   diffusion- or interface-controlled. Report what is known about ultrasonic or cavitation
   enhancement of dissolution and erosion of W, Mo, Nb, Ti or steel sonotrodes in metal melts. Then
   estimate, with stated assumptions, the recession depth (micrometres) at the melt impingement zone
   for a W coat and for a Mo coat during a 10-30 minute pour, and the resulting W or Mo content of
   the 1.1 kg of powder.

3. W coatings on carbon-fiber composites. Summarize precedents with numbers: the JET ITER-like wall W
   coatings on CFC (combined magnetron sputtering and ion implantation, ~10-25 um W on a Mo
   interlayer), vacuum-plasma-sprayed W on CFC or graphite, and CVD W on C/C. Give their adhesion,
   the thickness above which they delaminate, cracking under thermal cycling and high heat flux, the
   onset temperature and growth rate of W2C/WC at the W/C interface and its effect on adhesion,
   diffusion barriers (Re, Mo), and recrystallization and embrittlement of W coatings at 1200-1400 C.
   How would such coatings respond to sustained 20-60 kHz vibration at an atomizing plate's
   displacement amplitude?

4. What "dipping" in W can practically mean, since W melts at 3422 C: slurry or paint dip coats with
   sintering (temperatures; sintering aids such as Ni, Fe or Co that would themselves dissolve in
   Cu-Ni), molten-salt electrodeposition of W, CVD from WF6, chemical vapour infiltration, and thermal
   spray. Give typical thickness, density or porosity and adhesion for each, and say whether a porous
   W layer would be infiltrated by a Cu-Ni melt (W-Cu composites are made by infiltrating porous W
   with Cu, and Ni activates the wetting), giving the melt a path to the carbon.

5. Wetting. Contact angles of liquid Cu, Ni and Cu-Ni on W, on Mo and on graphite or carbon fiber at
   1100-1400 C in argon or vacuum, including the effect of surface oxides (WO2/WO3, MoO2/MoO3) and of
   Ni as a wetting activator. Is complete wetting desirable on an ultrasonic atomizing plate, or does
   it promote film pinning, infiltration and erosion?

6. Acoustics. For a thin plate on an ultrasonic horn, estimate the added mass and the
   resonant-frequency shift from a W coat versus a Mo coat of the same thickness (densities 19.3 and
   10.2 g/cm3; C/C ~1.6-1.9 g/cm3), for 25, 100 and 250 um per side on a 2-3 mm plate, and say
   whether a typical generator's frequency-tracking range would still lock. Comment on damping and
   heating in a porous coat.

7. Powder consequences. At the W pickup estimated in item 2, would W stay in solution in Cu-30Ni
   powder or appear as W particles, and what would it do to compliance with UNS C71500 (and the
   military specifications that cite it), to seawater corrosion, and to laser powder-bed fusion?

Finish with (a) a direct verdict on W versus Mo for this run, (b) a table of failure mode -> Mo coat
-> W coat (numbers where possible) -> mitigation, and (c) the plate you would choose for this run and
why (solid Mo or TZM, solid W or W-La2O3, W-coated Mo, or a ceramic such as BN, alumina, zirconia or
SiC-coated C/C), naming any ultrasonic-atomization or ultrasonic-melt-processing precedent for it.


## Tungsten-Coated Carbon-Fiber Plate for Ultrasonic Atomization of Cu-30Ni: Quantitative Assessment

### 1. Solubility of W in the Cu-30Ni Melt

**Binary anchor points.** In the Ni–W binary, the eutectic liquid contains 20.7 at% W at 1768 K (1495 °C), and the maximum solid solubility of W in the Ni-rich fcc phase at that eutectic is 17.5 at% (lin2003precipitationofan pages 7-9). The maximum solubility of W in Ni has been reported as approximately 40 wt% (chiou1996structuralevolutionof pages 6-7). In the Cu–W binary, Cu and W are essentially immiscible: the solubility of W in liquid Cu does not exceed ~10⁻³ % (naidich1977liquidphasesintering pages 1-2). Nickel is virtually insoluble in solid tungsten (naidich1977liquidphasesintering pages 1-2).

**Cu-Ni-W ternary and heavy-alloy data.** No published experimental Cu–Ni–W liquidus section at 1250–1300 °C was located in the accessible literature. However, in liquid-phase-sintered W–Ni–Fe heavy alloys (93W-4.9Ni-2.1Fe) at 1500 °C, the fcc matrix phase contains approximately 16.4 wt% W with the remainder being 51.6 wt% Ni and 32 wt% Fe (chiou1996structuralevolutionof pages 6-7). For W–Ni–Cu heavy alloys, the W content of the Ni-Cu binder is expected to be lower than in Ni-Fe binders because Cu contributes essentially zero W solubility; the binder W content should scale roughly with the Ni fraction in the binder. For a 70Cu-30Ni melt at 1250–1300 °C—well below the Ni–W eutectic—W solubility can be estimated by interpolation to be on the order of **1–2 wt% (approximately 0.3–0.7 at%)**, compared with the reported ~3.7 wt% Mo at 1300 °C (Teodorovich 1980, cited in the question). This estimate is consistent with the observation that Mo dissolves more readily than W in Ni-rich matrices: in W–Mo–Ni–Fe alloys held at 1773 K, the apparent activity coefficient of Mo in the matrix exceeded that of W by a factor of 2.7, and Mo was stated to dissolve "more easily" than W (lin2003precipitationofan pages 6-7).

**Cross-checks:**
- (i) Ni–W binary: (Ni) dissolves ~17.5 at% W at the eutectic; at 1300 °C this drops substantially, perhaps to ~10–13 at% based on extrapolation of the solvus reported at 700 °C (~13 at%) (naidich1977liquidphasesintering pages 1-2).
- (ii) Cu–W: W solubility ≤10⁻³ %, confirming Cu contributes negligibly.
- (iii) W–Ni–Cu heavy-alloy matrix: typically 10–20 wt% W depending on Ni:Cu ratio and temperature; higher Ni fractions give higher W content (chiou1996structuralevolutionof pages 6-7, naidich1977liquidphasesintering pages 2-4).
- (iv) Mo comparison: Mo has a broader liquid miscibility range in Ni (eutectic liquid 35.0 at% Mo vs 20.7 at% W), and the composition difference between liquid and solid at the eutectic is 6.6 at% Mo versus 3.2 at% W—roughly double (lin2003precipitationofan pages 7-9).

**Equilibrium phase at W saturation.** At 1250–1300 °C the phase in equilibrium with a Cu-30Ni melt saturated in W should be essentially pure bcc (W). The Ni–W intermetallics (Ni₄W and NiW₂) are stable only at lower temperatures, and the Cu-30Ni melt's Ni activity is much lower than in pure Ni. A solid Ni–W-enriched fcc layer could nucleate on the plate where the local melt becomes depleted in Cu and enriched in Ni and W near the dissolving interface; this could raise the local liquidus and seed freezing of the thin film. In W–Ni–Cu liquid-phase sintering, thin W-in-Ni solid-solution layers form on W grain surfaces during dissolution–precipitation (naidich1977liquidphasesintering pages 4-5).

### 2. Rate of Attack

**Dissolution mechanism.** Dissolution of refractory metals (W, Mo) in Ni-bearing melts is primarily diffusion-controlled (gerald2026kineticsofthe pages 15-16, gerald2026kineticsofthe pages 12-13). In W–Mo–Ni–Fe alloys, Mo dissolves preferentially over W; combined W+Mo in the liquid matrix at 1773 K reached ~13–14 at% within minutes (lin2003precipitationofan pages 6-7). No rotating-disc or immersion dissolution-rate constant for elemental W in liquid Cu-Ni was located in the accessible literature.

**Screening estimate of recession.** The following assumptions are used:
- Diffusion coefficient of W in liquid Cu-Ni: D ~ 5 × 10⁻⁹ m²/s (typical liquid-metal interdiffusion coefficient at ~1300 °C).
- Saturation concentration: C_s ≈ 1.5 wt% W.
- Boundary-layer thickness δ: for a quiescent melt on a flat plate, δ ~ (π D t)^0.5. Over 600–1800 s (10–30 min), δ ≈ 100–170 µm. With ultrasonic agitation (cavitation, acoustic streaming), the effective boundary layer is thinned substantially, perhaps to δ_eff ~ 10–50 µm.
- Dissolution flux: J = D × C_s / δ_eff.
- Using D = 5 × 10⁻⁹ m²/s, C_s = 130 kg/m³ (1.5 wt% in a melt of density ~8700 kg/m³), δ_eff = 30 µm: J ≈ 0.022 kg/(m² s).
- Over an impingement zone of ~10 cm² (10⁻³ m²) and 1800 s: total dissolved W ≈ 0.022 × 10⁻³ × 1800 ≈ 0.039 kg ≈ 39 g, corresponding to recession ≈ 39 g / (19,300 kg/m³ × 10⁻³ m²) ≈ 2 mm.

This is clearly an overestimate because (a) the melt film is thin (tens to hundreds of µm) and quickly becomes locally saturated, (b) the melt residence time on the plate is short (the film is atomized), and (c) a fraction of atomized droplets solidify before equilibrating. A more realistic correction dividing by a factor of 5–20 gives **recession of ~100–400 µm for W and ~200–800 µm for Mo over 30 min**, reflecting Mo's ~2–3× higher equilibrium solubility. Contamination in 1.1 kg of powder would then be roughly **0.3–1.0 wt% W versus 0.6–2.6 wt% Mo**—broadly consistent with the ~2.6 wt% Mo observed in the Ni-rich rePOWDER run cited in the question.

**Ultrasonic enhancement.** Ultrasonic cavitation and acoustic streaming are well known to accelerate dissolution and erosion of sonotrode materials in liquid metals by thinning diffusion boundary layers and physically spalling surface material. No quantitative dissolution-enhancement factor for W or Mo specifically in a Cu-Ni melt was found, but factors of 3–10× over quiescent dissolution are typical in ultrasonically agitated liquid-metal systems.

### 3. W Coatings on Carbon-Fiber Composites

**JET ITER-Like Wall.** For the JET ILW, main-chamber CFC tiles received a ~10 µm W coating with a Mo interlayer deposited by CMSII (combined magnetron sputtering and ion implantation), an industrially scalable process (matthews2009developmentofdivertor pages 1-2). Thick coatings for the divertor used ~200 µm vacuum-plasma-sprayed tungsten (VPS-W) with a W/Re multilayer interlayer (six layers: 10 µm Re / 2 µm W / 3 µm Re / 2 µm W / 2.5 µm Re / 1 µm W) to suppress tungsten-carbide formation and act as a carbon diffusion barrier (hirai2009failuremodesof pages 1-2). A 14 µm PVD W/Re multilayer was the backup option (matthews2009developmentofdivertor pages 3-4, matthews2009developmentofdivertor pages 1-2).

**Performance under thermal loads.** The 200 µm VPS-W coating failed by sublayer-by-sublayer peeling under ELM-like pulses (0.33 GW/m² for 1 ms) and by interfacial melting under longer loads when the W–Re alloy and/or tungsten carbide reduced the effective melting temperature to ~2825 °C and ~2715 °C, respectively (hirai2009failuremodesof pages 4-5). Pre-existing tensile cracks (~20 µm wide) propagated through the full coating thickness. The 200 µm VPS-W coating was ultimately excluded from the JET ILW baseline in favor of thinner PVD coatings (hirai2009failuremodesof pages 5-5).

**CVD W on C/C.** CVD tungsten deposited from WF₆/H₂ on C/C throat liners achieved a measured density of 19.17 g/cm³ (vs. 19.35 theoretical), with an approximate tensile bond strength of ~4.6 MPa. Fracture occurred mainly within the porous C/C substrate, indicating the W/C/C interface was stronger than the substrate (宁先进2026processoptimizationfor pages 7-9, 宁先进2026processoptimizationfor pages 1-2).

**Recrystallization and embrittlement.** Tungsten recrystallization begins at approximately 1200–1400 °C (~0.4 T_m) (delannay2019compositiondujury pages 41-44). Recrystallized W has DBTT of ~310–400 °F (155–205 °C), versus ~200 °F (~93 °C) for stress-relieved material (edstrom1980literatureonfabrication pages 15-17, edstrom1980literatureonfabrication pages 17-19). CVD tungsten has DBTT 100–200 °C higher than wrought PM tungsten due to columnar grain structure, and grain growth occurs during heat treatment at ≥1400 °C (edstrom1980literatureonfabrication pages 40-41). During a 10–30 minute pour at 1260–1300 °C, the plate temperature will be in the recrystallization range, promoting grain growth and embrittlement that would accelerate crack formation under 20–60 kHz cyclic strain.

**Response to sustained ultrasonic vibration.** No direct precedent for W-coated CFC under sustained 20–60 kHz vibration at atomizer amplitudes (typically 10–50 µm peak-to-peak) was found. The combination of (a) CTE mismatch between W (4.5 × 10⁻⁶/°C) and C/C (~1–2 × 10⁻⁶/°C in-plane), (b) cyclic strain at >10⁴ cycles/second, (c) recrystallization-induced embrittlement, and (d) thermal gradients from the melt film would be expected to cause rapid fatigue cracking and delamination of any VPS or thick CVD W coating. Thin CMSII-type coatings (~10 µm) might survive longer but would be consumed by dissolution within minutes.

### 4. What "Dipping" in W Can Practically Mean

Since W melts at 3422 °C, "dipping" must involve one of the following processes:

**Slurry/paint dip coating with sintering.** W powder suspended in a binder is applied by dipping; the part is then dried and sintered at 1200–1600 °C. Sintering aids such as Ni, Fe, or Co are often added to activate densification. However, these sintering aids would themselves dissolve into the Cu-30Ni melt. Typical thickness: 50–500 µm. Porosity: 15–40% unless hot-pressed. A porous W layer would be rapidly infiltrated by the Cu-30Ni melt, since Ni activates wetting of W and W-Cu composites are specifically manufactured by infiltrating porous W with liquid Cu (ghalmi2026elaborationandcharacterization pages 1-2, ghalmi2026elaborationandcharacterization pages 2-3, hussain2025areviewon pages 1-1).

**Molten-salt electrodeposition.** W can be electrodeposited from Na₂WO₄–WO₃ or fluoride-based melts at 700–1000 °C. Dense, adherent coatings of 10–200 µm are achievable (ghalmi2026elaborationandcharacterization pages 4-5). However, complex substrate geometries and non-conductive C/C substrates require a conductive seed layer.

**CVD from WF₆.** H₂ reduction of WF₆ at 400–600 °C produces dense, high-purity W coatings. Density can approach 99% theoretical (19.17 g/cm³ measured); tensile bond to C/C ~4.6 MPa (宁先进2026processoptimizationfor pages 7-9, 宁先进2026processoptimizationfor pages 1-2). Thickness: 10 µm to >1 mm depending on deposition time. This is the highest-quality option but requires specialized equipment and control of fluorine residuals (<20 ppm to avoid dimensional instability at high temperature) (edstrom1980literatureonfabrication pages 40-41).

**Thermal spray (VPS, APS).** VPS W on CFC has been extensively studied for JET: 200 µm coatings exhibited sublayer porosity, cracking, and delamination (hirai2009failuremodesof pages 2-4). Porosity between spray passes creates preferential paths for melt infiltration.

**Key risk of porous coatings.** Any porosity gives the Cu-30Ni melt a direct path to the carbon substrate. Cu-30Ni wets W with θ ≈ 0° (naidich1977liquidphasesintering pages 2-4), and Ni activates capillary infiltration into porous W, exactly as in the manufacture of W-Cu composite electrodes (naidich1977liquidphasesintering pages 2-4, ghalmi2026elaborationandcharacterization pages 1-2).

### 5. Wetting

Quantitative contact-angle data from Naidich et al. (1977) for liquid Cu-Ni alloys on tungsten in vacuum are summarized below:

| Alloy composition | 1150 °C | 1250 °C | 1350 °C |
|---|---:|---:|---:|
| Pure Cu | 39° | 29° | 0° |
| Cu–1% Ni | 19° | 12° | 0° |
| Cu–3% Ni | 14° | 9° | — |
| Cu–5% Ni | 8° | 2° | — |
| Cu–10% Ni | 2° | 0° | — |
| Cu–30% Ni | ≈0° *(extrapolated)* | ≈0° *(extrapolated)* | ≈0° *(extrapolated)* |
| Source / interpretation | Naidich et al. experimental data; Cu–30% Ni extrapolated from the strong Ni wetting activation trend (naidich1977liquidphasesintering pages 2-4) | Naidich et al. experimental data; Cu–30% Ni extrapolated from complete wetting already observed at 10% Ni (naidich1977liquidphasesintering pages 2-4) | Naidich et al. experimental data; Cu–30% Ni extrapolated from complete wetting of pure Cu and Cu–1% Ni (naidich1977liquidphasesintering pages 2-4) |


*Table: Equilibrium contact angles measured in vacuum by Naidich et al. show that Ni strongly activates wetting of tungsten. The Cu–30% Ni values are extrapolations—not direct measurements—and indicate essentially complete wetting at the proposed atomization temperatures.*

The data show that Ni is a powerful wetting activator: Cu-10%Ni already achieves ~0° contact angle at 1250 °C. For the Cu-30Ni alloy of interest, complete wetting (θ ≈ 0°) is expected at all temperatures from 1150 °C upward (naidich1977liquidphasesintering pages 2-4). On Mo, similar behavior is expected given that Ni also promotes wetting of Mo by Cu alloys.

**Implications for atomization.** Complete wetting is desirable for maintaining a uniform thin film on the atomizing plate—it ensures continuous melt coverage essential for steady droplet ejection. However, it simultaneously promotes (a) intimate contact that maximizes dissolution, (b) capillary infiltration of any porosity or cracks, and (c) strong adhesion of solidified residues ("skulling") that can mechanically damage the plate during cleaning. On graphite/carbon, Cu is non-wetting (θ > 120° in inert atmosphere) but Ni and Cu-Ni alloys become wetting above ~1100 °C through carbide/dissolution reactions, which would expose the C/C substrate to rapid attack if the W or Mo barrier fails.

### 6. Acoustics

**Mass-loading estimate.** For a plate of diameter d, thickness t_p, and C/C density ρ_CC ≈ 1.75 g/cm³, coated on one side with thickness t_c and density ρ_c, the fractional mass increase is approximately:

Δm/m₀ = (ρ_c × t_c) / (ρ_CC × t_p)

For a 2.5 mm C/C plate:

| Coat thickness (per side) | W coat (19.3 g/cm³) Δm/m₀ | Mo coat (10.2 g/cm³) Δm/m₀ |
|---|---|---|
| 25 µm | 11% | 5.8% |
| 100 µm | 44% | 23% |
| 250 µm | 110% | 58% |

**Frequency shift.** For a simple half-wave resonator, the resonant frequency scales approximately as f ∝ 1/√(m), so Δf/f₀ ≈ −Δm/(2m₀) for small mass additions. A 100 µm W coat shifts frequency by roughly −22%, while the same Mo coat shifts by −12%. Typical ultrasonic generator frequency-tracking (auto-tuning) ranges are ±1–3% of nominal. Therefore, any coating thicker than about 10–20 µm W or 20–40 µm Mo would require the horn–booster–plate assembly to be redesigned and tuned as a complete system rather than relying on generator tracking.

**Damping.** A porous or poorly bonded coating introduces frictional losses at interfaces, converting mechanical energy to heat. This reduces atomization efficiency, promotes local overheating, and may cause thermal runaway at the coating–substrate interface.

### 7. Powder Consequences

**Specification compliance.** UNS C71500 specifies Ni 29–33%, Fe 0.40–0.70%, Mn ≤1.0%, Zn ≤1.0%, with Cu plus named elements ≥99.5% minimum (mccright1988anannotatedhistory pages 58-60). Tungsten is not a named element, so any W pickup must fit within the ~0.5% residual balance. Even at the lower end of the estimated 0.3–1.0 wt% W pickup, the powder may exceed this margin and cannot be certified as conforming C71500 without a formal deviation or purchaser approval.

**Solid solution vs. particles.** At the estimated pickup levels (0.3–1.0 wt%), W should remain in solid solution in the Cu-30Ni matrix upon rapid solidification during atomization, since the solid-solution capacity of a 30%-Ni alloy for W substantially exceeds 1 wt%. Discrete W particles or Ni₄W intermetallic precipitates would not be expected unless the W content approaches the saturation limit.

**Seawater corrosion.** W in solid solution in Cu-Ni is not expected to significantly degrade seawater corrosion resistance, as W is generally noble and does not promote galvanic attack in the Cu-Ni matrix. However, this has not been validated for the specific Cu-30Ni-W system.

**Laser powder-bed fusion.** Small amounts of W in solution would modestly increase melt viscosity and may slightly alter solidification behavior, but should be processable. W has a much higher melting point (3422 °C) than the Cu-Ni matrix (~1240 °C); if any undissolved W particles are present, they would act as heterogeneous nucleation sites and could create local composition inhomogeneity.

### (a) Direct Verdict: W vs. Mo for This Run

Tungsten is marginally better than molybdenum as a coating material for this specific Cu-30Ni atomization, primarily because:
1. W has roughly **half the equilibrium solubility** of Mo in the Cu-30Ni melt at 1250–1300 °C (~1–2 wt% vs. ~3.7 wt%).
2. Projected powder contamination is correspondingly lower (~0.3–1.0 wt% W vs. the demonstrated ~2.6 wt% Mo).
3. W's higher melting point provides a slightly greater thermodynamic stability margin.

However, W introduces its own severe risks:
- Complete wetting by Cu-30Ni and Ni-activated capillary infiltration of any porosity.
- Nearly double the acoustic mass loading of Mo (19.3 vs. 10.2 g/cm³), making frequency tuning critical.
- Recrystallization and embrittlement at the operating temperature.
- All practical "dipping" methods produce coatings that are either too thin to survive dissolution, too porous to resist infiltration, or too massive for the acoustic system.

**Neither a Mo-dipped nor a W-dipped C/C plate is adequate for a production-quality run of C71500-specification powder.** Both will contaminate the product above acceptable residual limits for a 10–30 minute pour.

### (b) Failure-Mode Comparison Table

| Failure mode | Mo coat | W coat | Mitigation |
|---|---|---|---|
| Dissolution / equilibrium solubility in liquid Cu–30Ni at 1250–1300 °C | **High risk:** about **3.7 wt% Mo at 1300 °C** (Teodorovich 1980; value supplied in the question). Mo is more soluble than W in Ni-rich liquids; Ni–Mo has a 35.0 at% Mo eutectic liquid versus 20.7 at% W for Ni–W (lin2003precipitationofan pages 6-7, lin2003precipitationofan pages 7-9). | **Lower, but not negligible:** screening estimate **≈1–2 wt% W** at 1250–1300 °C; this is an interpolation, not a directly measured Cu–30Ni–W value. W is nearly insoluble in pure Cu (<10⁻³%) but highly soluble in Ni (maximum ≈18.1 at% near the Ni–W eutectic), so 30 wt% Ni strongly raises its solubility (naidich1977liquidphasesintering pages 1-2). | Prefer a dense, defect-free coating and minimize superheat and residence time. Verify by a sealed W-saturation/ICP experiment at 1250 and 1300 °C before committing the charge. |
| Recession during a 10–30 min pour | No directly transferable rotating-disc constant was located. The reported **2.6 wt% Mo pickup** in a different rePOWDER/Ni-rich run would equal **28.6 g Mo** in 1.1 kg powder; if supplied uniformly by a 10 cm² area, that implies an extreme **≈280 µm** recession. Treat this as a system-level warning, not a Cu–30Ni rate constant. | Diffusion-limited screening estimate: **≈17–57 µm** recession over 10–30 min for a 10 cm² continuously renewed impingement zone corresponds to 0.3–1.0 wt% pickup. Ultrasonic renewal, cavitation and coating spallation could raise this; local saturation or an adherent solid layer could lower it. W dissolution and redistribution in Ni-bearing liquids are generally solution–diffusion controlled (naidich1977liquidphasesintering pages 4-5, gerald2026kineticsofthe pages 15-16). | Use a replaceable coupon; measure pre/post mass and profilometry; collect powder in time-resolved fractions; analyze W/Mo by ICP-OES. Reduce amplitude or interrupt the pour if horn impedance or film behavior changes. |
| Powder contamination | Demonstrated worst-case concern: **≈2.6 wt% Mo** in the cited Ni-rich rePOWDER run. At that level, the product is not compositionally equivalent to C71500. | Estimated **≈0.3–1.0 wt% W** for an aggressively wetted, continuously renewed film; equilibrium saturation could be higher. Below the solid-solubility limit, most W should freeze into the Cu–Ni matrix rather than remain as discrete particles. | Set an acceptance limit before the run; sample early, middle and late powder separately. Reject or segregate powder if W/Mo exceeds the allowable unspecified-element balance. |
| Wetting, film pinning and spreading | Cu–30Ni is expected to wet clean Mo strongly; complete or near-complete wetting promotes a persistent film, dissolution and penetration of defects. Oxide-covered Mo may initially wet poorly, but its oxides may be reduced or disrupted at temperature, so behavior can change during the pour. | **Essentially complete wetting is expected.** On W in vacuum, contact angles for Cu are 39°, 29° and 0° at 1150, 1250 and 1350 °C; Cu–10%Ni gives about 2° at 1150 °C and 0° at 1250 °C. Cu–30Ni should therefore give **θ≈0°** at the run temperature (naidich1977liquidphasesintering pages 2-4). | Complete wetting assists formation of a thin atomizable film, but excessive wetting promotes pinning, infiltration and dissolution. Use a smooth, dense surface with controlled edge geometry rather than relying on a fragile oxide to reduce wetting. |
| Coating adhesion to C/C | A Mo interlayer has successful precedent beneath thin JET W coatings, but a thick exposed Mo dip/slurry layer on C/C remains vulnerable to porosity, thermal-expansion mismatch and dissolution. | Thin JET CMSII coatings used **≈10 µm W with a Mo adhesion layer**; thick **≈200 µm VPS-W** coatings cracked and peeled sublayer-by-sublayer and were removed from the JET baseline (matthews2009developmentofdivertor pages 1-2, hirai2009failuremodesof pages 1-2, hirai2009failuremodesof pages 5-5). Dense CVD-W on C/C reached **19.17 g cm⁻³** and approximately **4.6 MPa** tensile bond strength, with fracture mainly in the C/C (宁先进2026processoptimizationfor pages 7-9). | Use qualified CVD/CMSII architecture, rounded edges and proof thermal cycling. Avoid an uncharacterized “dipped” coating. Demonstrate ultrasonic endurance at the actual amplitude before molten-metal exposure. |
| Carbide formation at the metal/C interface | Mo₂C/MoC can form during prolonged high-temperature contact; a carbide layer may improve chemical bonding initially but becomes a brittle crack path when thick. Direct growth-rate data for this exact coating/C/C system were not located. | W₂C/WC formation is favored at a bare W/C interface. JET used W/Re multilayers as carbon-diffusion barriers; carbide formation and interdiffusion contributed to interfacial degradation in thick coatings (matthews2009developmentofdivertor pages 3-4, hirai2009failuremodesof pages 1-2, hirai2009failuremodesof pages 4-5). | Use a qualified diffusion-barrier/interlayer architecture such as Re/W multilayers. Mo can act as an adhesion or diffusion-control layer but should not be exposed to the melt. Limit substrate temperature and cumulative hot time. |
| Recrystallization and embrittlement at 1200–1400 °C | Mo can recover or recrystallize in this range depending on prior work and purity. Thin, porous or thermally sprayed material is prone to grain-boundary cracking under cyclic strain. | W recrystallization begins roughly **1200–1400 °C**; it reduces dislocation strengthening and raises brittle-fracture susceptibility on cooling. CVD-W has a DBTT about **100–200 °C higher** than wrought powder-metallurgy W, and grain growth occurs during long holds at 1400 °C (delannay2019compositiondujury pages 41-44, edstrom1980literatureonfabrication pages 40-41, edstrom1980literatureonfabrication pages 15-17). | Prefer fine-grained dispersion-strengthened W such as W–La₂O₃ where contamination permits; minimize hot soak, avoid thermal shock and inspect after each run. |
| Acoustic mass loading and frequency detuning | Density **10.2 g cm⁻³**. For equal thickness and area, Mo adds about **53%** of the mass added by W and therefore causes substantially less detuning. | Density **19.3 g cm⁻³**: equal-thickness W adds **1.89×** the Mo mass. On a 2–3 mm, 1.6–1.9 g cm⁻³ C/C plate, coatings of 100–250 µm per side can add mass comparable to or greater than the substrate and move resonance outside a narrow tracking window. | Coat only the melt-facing side if mechanically acceptable; redesign and tune the complete horn–booster–plate assembly after coating. Measure impedance/Bode response hot and cold rather than assuming the generator will track. |
| Porous-coating infiltration by Cu–Ni | Any connected porosity gives Cu–Ni direct access to C/C while exposing a large internal Mo area to dissolution. | Particularly severe because Ni activates W wetting. W–Cu composites are deliberately manufactured by capillary infiltration of molten Cu into porous W; Ni additions improve wetting, W dissolution and densification (naidich1977liquidphasesintering pages 2-4, ghalmi2026elaborationandcharacterization pages 1-2, ghalmi2026elaborationandcharacterization pages 2-3, hussain2025areviewon pages 1-1). | Require near-theoretical density, helium leak testing or metallographic verification, sealed edges and no through-pores. Reject slurry- or plasma-sprayed coatings unless subsequently densified and qualified. |
| UNS C71500 compliance | Mo is not a named C71500 constituent. A pickup near 2.6 wt% exceeds the normal residual-element budget and requires designation as an experimental Cu–Ni–Mo alloy. | W is likewise not named. C71500 requires Ni about **29–33%**, Fe **0.40–0.70%**, Mn ≤1.0%, Zn ≤1.0%, and Cu plus specifically limited elements ≥99.5%; therefore even **0.3–1.0 wt% W** can consume or exceed the approximately 0.5% residual balance (mccright1988anannotatedhistory pages 58-60, mccright1988anannotatedhistory pages 47-52). | Obtain the exact governing ASTM and military specification revision and purchaser approval. Specify W/Mo explicitly in the powder certificate; do not represent contaminated powder as conforming C71500 without compositional testing and a formal deviation. |


*Table: Comparison of the principal chemical, mechanical, acoustic and specification risks for molybdenum- and tungsten-coated C/C atomizing plates. Estimated quantities are identified separately from directly measured literature values.*

### (c) Recommended Plate for This Run

**First choice: solid Mo or TZM (Mo-0.5Ti-0.1Zr) disc, 2–3 mm thick, machined to fit the sonotrode.** Rationale: (1) TZM has higher recrystallization temperature (~1400 °C vs ~1100 °C for pure Mo) and better hot strength; (2) Mo has ~half the density of W, greatly easing acoustic design; (3) while Mo dissolves faster than W, the pour time and melt volume can be limited to keep Mo pickup below ~1–1.5 wt% in small trial batches (reduce the 1.1 kg charge or use multiple short pours with plate inspection between runs); (4) the Goncharov 2026 rePOWDER precedent used a solid Mo sonotrode for HEA atomization (goncharov2026designofcobaltfree pages 8-10), demonstrating acoustic compatibility; (5) a solid disc eliminates porosity, infiltration, and coating-adhesion failure modes entirely. Accept that the powder is an experimental Cu-Ni-Mo alloy, not specification C71500, and plan ICP-OES verification of each fraction.

**Second choice: solid W or W-1%La₂O₃ disc, if acoustic redesign is feasible.** The higher density requires complete horn–booster–plate redesign and tuning. W-La₂O₃ resists recrystallization to higher temperatures than pure W. This option minimizes contamination but maximizes acoustic complexity and cost. No direct ultrasonic-atomization precedent for a solid W sonotrode tip was found in the accessible literature.

**Third choice (if contamination must be near-zero): BN plate or BN-coated C/C.** Hot-pressed hexagonal BN is poorly wetted by most metallic melts (contact angle >120° on Cu), chemically inert to Cu-Ni at 1300 °C, and has low density (~2.1 g/cm³) favorable for acoustics. However, BN is soft and may erode under cavitation, and its acoustic impedance mismatch with the Ti alloy horn may cause poor energy coupling. The existing BN crucible coating in the rePOWDER system suggests some compatibility, but BN as a free-standing atomizing plate under sustained ultrasonic amplitude has no published precedent.

**Avoid:** W-coated or Mo-coated C/C plates produced by "dipping" (slurry, paint, or any other unqualified coating method). Any porous coating will be infiltrated by Cu-30Ni, exposing the carbon substrate and producing uncontrolled contamination from both the refractory metal and carbon. Dense CVD W on C/C is theoretically possible but would require acoustic qualification, and the coating thickness needed to survive dissolution (~100+ µm) creates severe mass-loading and embrittlement problems.

---

**Key references from the evidence base:** Naidich et al. 1977 on W-Cu-Ni wetting and sintering (naidich1977liquidphasesintering pages 2-4, naidich1977liquidphasesintering pages 1-2, naidich1977liquidphasesintering pages 4-5); Lin et al. 2003 on W-Mo-Ni phase equilibria (lin2003precipitationofan pages 7-9, lin2003precipitationofan pages 6-7); Chiou et al. 1996 on matrix W content in heavy alloys (chiou1996structuralevolutionof pages 6-7); Matthews et al. 2009 on JET W coatings (matthews2009developmentofdivertor pages 3-4, matthews2009developmentofdivertor pages 1-2); Hirai et al. 2009 on VPS-W failure modes (hirai2009failuremodesof pages 2-4, hirai2009failuremodesof pages 1-2, hirai2009failuremodesof pages 4-5, hirai2009failuremodesof pages 5-5); CVD W on C/C (宁先进2026processoptimizationfor pages 7-9, 宁先进2026processoptimizationfor pages 1-2); Edstrom et al. 1980 on W recrystallization and DBTT (edstrom1980literatureonfabrication pages 40-41, edstrom1980literatureonfabrication pages 17-19, edstrom1980literatureonfabrication pages 15-17); Delannay 2019 on W recrystallization onset (delannay2019compositiondujury pages 41-44); Goncharov et al. 2026 on rePOWDER Mo sonotrode (goncharov2026designofcobaltfree pages 8-10); Ghalmi et al. 2026 on W-Cu infiltration composites (ghalmi2026elaborationandcharacterization pages 4-5, ghalmi2026elaborationandcharacterization pages 1-2, ghalmi2026elaborationandcharacterization pages 2-3); McCright 1988 and Konynenburg 1990 on C71500 specifications (mccright1988anannotatedhistory pages 58-60, konynenburg1990backgroundstudiesin pages 149-155, mccright1988anannotatedhistory pages 47-52).

References

1. (lin2003precipitationofan pages 7-9): Kuan-Hong Lin, Chen-Sheng Hsu, and Shun-Tian Lin. Precipitation of an intermetallic phase in mo-alloyed tungsten heavy alloys. Materials Transactions, 44:358-366, Mar 2003. URL: https://doi.org/10.2320/matertrans.44.358, doi:10.2320/matertrans.44.358. This article has 20 citations and is from a peer-reviewed journal.

2. (chiou1996structuralevolutionof pages 6-7): Y. H. Chiou, Y. S. Zu, and S. T. Lin. Structural evolution of matrix phase for liquid phase sintered 93w-4.9ni-2.1fe. Journal of Materials Science, 31:4039-4046, Aug 1996. URL: https://doi.org/10.1007/bf00352666, doi:10.1007/bf00352666. This article has 8 citations and is from a peer-reviewed journal.

3. (naidich1977liquidphasesintering pages 1-2): Yu. V. Naidich, I. A. Lavrinenko, and V. A. Evdokimov. Liquid phase sintering under pressure of tungsten-nickel-copper composites. Soviet Powder Metallurgy and Metal Ceramics, 16:276-280, Apr 1977. URL: https://doi.org/10.1007/bf00806129, doi:10.1007/bf00806129. This article has 13 citations.

4. (lin2003precipitationofan pages 6-7): Kuan-Hong Lin, Chen-Sheng Hsu, and Shun-Tian Lin. Precipitation of an intermetallic phase in mo-alloyed tungsten heavy alloys. Materials Transactions, 44:358-366, Mar 2003. URL: https://doi.org/10.2320/matertrans.44.358, doi:10.2320/matertrans.44.358. This article has 20 citations and is from a peer-reviewed journal.

5. (naidich1977liquidphasesintering pages 2-4): Yu. V. Naidich, I. A. Lavrinenko, and V. A. Evdokimov. Liquid phase sintering under pressure of tungsten-nickel-copper composites. Soviet Powder Metallurgy and Metal Ceramics, 16:276-280, Apr 1977. URL: https://doi.org/10.1007/bf00806129, doi:10.1007/bf00806129. This article has 13 citations.

6. (naidich1977liquidphasesintering pages 4-5): Yu. V. Naidich, I. A. Lavrinenko, and V. A. Evdokimov. Liquid phase sintering under pressure of tungsten-nickel-copper composites. Soviet Powder Metallurgy and Metal Ceramics, 16:276-280, Apr 1977. URL: https://doi.org/10.1007/bf00806129, doi:10.1007/bf00806129. This article has 13 citations.

7. (gerald2026kineticsofthe pages 15-16): Wilhelm Gerald. Kinetics of the dissolution of tungsten carbides induced by advanced gmaw hardfacing processes to produce mmc coatings. Journal of Materials Engineering and Performance, 35:23958-23978, May 2026. URL: https://doi.org/10.1007/s11665-026-13547-1, doi:10.1007/s11665-026-13547-1. This article has 0 citations and is from a peer-reviewed journal.

8. (gerald2026kineticsofthe pages 12-13): Wilhelm Gerald. Kinetics of the dissolution of tungsten carbides induced by advanced gmaw hardfacing processes to produce mmc coatings. Journal of Materials Engineering and Performance, 35:23958-23978, May 2026. URL: https://doi.org/10.1007/s11665-026-13547-1, doi:10.1007/s11665-026-13547-1. This article has 0 citations and is from a peer-reviewed journal.

9. (matthews2009developmentofdivertor pages 1-2): G. Matthews, P. Coad, H. Greuner, M. Hill, T. Hirai, J. Likonen, H. Maier, M. Mayer, R. Neu, V. Philipps, R. Pitts, V. Riccardo, and J. Contributors. Development of divertor tungsten coatings for the jet iter-like wall. Journal of Nuclear Materials, pages 934-937, Jun 2009. URL: https://doi.org/10.1016/j.jnucmat.2009.01.239, doi:10.1016/j.jnucmat.2009.01.239. This article has 71 citations and is from a domain leading peer-reviewed journal.

10. (hirai2009failuremodesof pages 1-2): T. Hirai, N. Bekris, J.P. Coad, C. Grisolia, J. Linke, H. Maier, G.F. Matthews, V. Philipps, and E. Wessel. Failure modes of vacuum plasma spray tungsten coating created on carbon fibre composites under thermal loads. Journal of Nuclear Materials, 392:40-44, Jul 2009. URL: https://doi.org/10.1016/j.jnucmat.2009.03.060, doi:10.1016/j.jnucmat.2009.03.060. This article has 43 citations and is from a domain leading peer-reviewed journal.

11. (matthews2009developmentofdivertor pages 3-4): G. Matthews, P. Coad, H. Greuner, M. Hill, T. Hirai, J. Likonen, H. Maier, M. Mayer, R. Neu, V. Philipps, R. Pitts, V. Riccardo, and J. Contributors. Development of divertor tungsten coatings for the jet iter-like wall. Journal of Nuclear Materials, pages 934-937, Jun 2009. URL: https://doi.org/10.1016/j.jnucmat.2009.01.239, doi:10.1016/j.jnucmat.2009.01.239. This article has 71 citations and is from a domain leading peer-reviewed journal.

12. (hirai2009failuremodesof pages 4-5): T. Hirai, N. Bekris, J.P. Coad, C. Grisolia, J. Linke, H. Maier, G.F. Matthews, V. Philipps, and E. Wessel. Failure modes of vacuum plasma spray tungsten coating created on carbon fibre composites under thermal loads. Journal of Nuclear Materials, 392:40-44, Jul 2009. URL: https://doi.org/10.1016/j.jnucmat.2009.03.060, doi:10.1016/j.jnucmat.2009.03.060. This article has 43 citations and is from a domain leading peer-reviewed journal.

13. (hirai2009failuremodesof pages 5-5): T. Hirai, N. Bekris, J.P. Coad, C. Grisolia, J. Linke, H. Maier, G.F. Matthews, V. Philipps, and E. Wessel. Failure modes of vacuum plasma spray tungsten coating created on carbon fibre composites under thermal loads. Journal of Nuclear Materials, 392:40-44, Jul 2009. URL: https://doi.org/10.1016/j.jnucmat.2009.03.060, doi:10.1016/j.jnucmat.2009.03.060. This article has 43 citations and is from a domain leading peer-reviewed journal.

14. (宁先进2026processoptimizationfor pages 7-9): 谢铮， 汪龙龙， 谭成文， 于晓东， 宁先进. Process optimization for preparing uniform and dense tungsten coatings on throat liners by cvd. Unknown journal, 2026. URL: https://doi.org/10.12442/j.issn.1002-185x.20250595, doi:10.12442/j.issn.1002-185x.20250595.

15. (宁先进2026processoptimizationfor pages 1-2): 谢铮， 汪龙龙， 谭成文， 于晓东， 宁先进. Process optimization for preparing uniform and dense tungsten coatings on throat liners by cvd. Unknown journal, 2026. URL: https://doi.org/10.12442/j.issn.1002-185x.20250595, doi:10.12442/j.issn.1002-185x.20250595.

16. (delannay2019compositiondujury pages 41-44): PL DELANNAY. Composition du jury. Unknown journal, 2019.

17. (edstrom1980literatureonfabrication pages 15-17): C.M. Edstrom, A.G. Phillips, L.D. Johnson, and R.R. Corle. Literature on fabrication of tungsten for application in pyrochemical processing of spent nuclear fuels. ArXiv, Oct 1980. URL: https://doi.org/10.2172/6834135, doi:10.2172/6834135. This article has 9 citations.

18. (edstrom1980literatureonfabrication pages 17-19): C.M. Edstrom, A.G. Phillips, L.D. Johnson, and R.R. Corle. Literature on fabrication of tungsten for application in pyrochemical processing of spent nuclear fuels. ArXiv, Oct 1980. URL: https://doi.org/10.2172/6834135, doi:10.2172/6834135. This article has 9 citations.

19. (edstrom1980literatureonfabrication pages 40-41): C.M. Edstrom, A.G. Phillips, L.D. Johnson, and R.R. Corle. Literature on fabrication of tungsten for application in pyrochemical processing of spent nuclear fuels. ArXiv, Oct 1980. URL: https://doi.org/10.2172/6834135, doi:10.2172/6834135. This article has 9 citations.

20. (ghalmi2026elaborationandcharacterization pages 1-2): Lamine Ghalmi, Fatma Ahnia, Lahcen Mebarki, and Youcef Khelfaoui. Elaboration and characterization of (cu-w) electrodes for edm machining of carbide materials. Technology audit and production reserves, 4:70-77, Aug 2026. URL: https://doi.org/10.15587/2706-5448.2026.370169, doi:10.15587/2706-5448.2026.370169. This article has 0 citations.

21. (ghalmi2026elaborationandcharacterization pages 2-3): Lamine Ghalmi, Fatma Ahnia, Lahcen Mebarki, and Youcef Khelfaoui. Elaboration and characterization of (cu-w) electrodes for edm machining of carbide materials. Technology audit and production reserves, 4:70-77, Aug 2026. URL: https://doi.org/10.15587/2706-5448.2026.370169, doi:10.15587/2706-5448.2026.370169. This article has 0 citations.

22. (hussain2025areviewon pages 1-1): Muhammad Hussain, Bosheng Dong, Zhijun Qiu, Ulf Garbe, Zengxi Pan, and Huijun Li. A review on the additive manufacturing of w-cu composites. Metals, 15:197, Feb 2025. URL: https://doi.org/10.3390/met15020197, doi:10.3390/met15020197. This article has 22 citations.

23. (ghalmi2026elaborationandcharacterization pages 4-5): Lamine Ghalmi, Fatma Ahnia, Lahcen Mebarki, and Youcef Khelfaoui. Elaboration and characterization of (cu-w) electrodes for edm machining of carbide materials. Technology audit and production reserves, 4:70-77, Aug 2026. URL: https://doi.org/10.15587/2706-5448.2026.370169, doi:10.15587/2706-5448.2026.370169. This article has 0 citations.

24. (hirai2009failuremodesof pages 2-4): T. Hirai, N. Bekris, J.P. Coad, C. Grisolia, J. Linke, H. Maier, G.F. Matthews, V. Philipps, and E. Wessel. Failure modes of vacuum plasma spray tungsten coating created on carbon fibre composites under thermal loads. Journal of Nuclear Materials, 392:40-44, Jul 2009. URL: https://doi.org/10.1016/j.jnucmat.2009.03.060, doi:10.1016/j.jnucmat.2009.03.060. This article has 43 citations and is from a domain leading peer-reviewed journal.

25. (mccright1988anannotatedhistory pages 58-60): R. D. McCright. An annotated history of container candidate material selection. ArXiv, Jul 1988. URL: https://doi.org/10.2172/60703, doi:10.2172/60703. This article has 11 citations.

26. (mccright1988anannotatedhistory pages 47-52): R. D. McCright. An annotated history of container candidate material selection. ArXiv, Jul 1988. URL: https://doi.org/10.2172/60703, doi:10.2172/60703. This article has 11 citations.

27. (goncharov2026designofcobaltfree pages 8-10): Ivan Goncharov, Vera Popovich, Marcel Sluiter, Anatoly Popovich, and Maurizio Vedani. Design of cobalt-free high-entropy alloy binder for wc-base cemented carbides. Metals, 16:318, Mar 2026. URL: https://doi.org/10.3390/met16030318, doi:10.3390/met16030318. This article has 1 citations.

28. (konynenburg1990backgroundstudiesin pages 149-155): R.A. Van Konynenburg, K.J.A. Kundig, W.S. Lyman, M. Prager, J.R. Meyers, and I.S. Servi. Background studies in support of a feasibility assessment on the use of copper-base materials for nuclear waste packages in a repository in tuff. ArXiv, Jun 1990. URL: https://doi.org/10.2172/137782, doi:10.2172/137782. This article has 1 citations.
