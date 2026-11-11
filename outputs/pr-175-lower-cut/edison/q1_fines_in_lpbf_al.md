# Edison job-futurehouse-paperqa3-high result: q1_fines_in_lpbf_al

**Task ID:** `70c4d713-bf40-45b4-9927-3d35eed42a4b`  
**Status:** success

<details><summary>Query</summary>

```text
Context. A university lab ultrasonically atomizes aluminium alloys (Al 4047 / AlSi12 and 6063) on an
AMAZEMET rePOWDER (about 40 kHz, molybdenum plate) in 100-250 g runs, for laser powder bed fusion on an
Aconity MIDI. The powder is highly spherical. An SEM image-analysis PSD of a nickel-aluminium bronze from the
same atomizer (5,937 particles) gave number D10/D50/D90 of 35/47/72 um and volume D10/D50/D90 of
46/104/209 um, with 2.1 % by number and under 0.1 % by volume below 20 um. A first SEM look at the Al lots
found the smallest particles mostly 40-60 um. The lab has 8 in (200 mm) stainless test sieves at 250 um
(No. 60) and 63 um (No. 230), with 45 um (No. 325) on order, and no sieve shaker yet. The runs plan targets a
15-45 um window; an earlier plan targeted 20-63 um.

Question: does the sub-15/20 um fraction matter for LPBF of aluminium alloys, and is "no lower cut" defensible?
Use experimental papers and give numbers with sources.

1. Measured effects of fines (below 15-20 um) in Al alloy LPBF powders (AlSi10Mg, AlSi12, AlSi7Mg, 4047,
   6061/6063, Scalmalloy) on flowability (Hall/Carney flow, avalanche angle, revolution powder analysis,
   Hausner ratio, FT4 cohesion), spreadability and layer quality (blade, roller, brush or rubber recoaters),
   packing density, spatter and denudation, porosity (lack of fusion, keyhole), surface roughness, powder
   oxygen and hydrogen, and tensile properties. Which studies varied the fines content of one Al powder
   (blended fines, 0-63 vs 20-63 vs 15-45 um, or recycled powder that lost its fines), and what fines fraction
   (by volume and by number) changed the outcome? Explain the cohesion argument (granular Bond number,
   van der Waals versus weight) for Al at its low density, at 10, 20 and 45 um.
2. What do LPBF and powder papers on ultrasonically atomized powders (Al especially; AMAZEMET rePOWDER, ATO
   Lab/Lab+, other ultrasonic atomizers; e.g. Yankin 2025, Priyadarshi 2024, Ukabhai 2025, Balasz 2023/2024,
   Hinrichs 2021, Zrodowski, Pilarski, Kaminski) actually do: an upper cut only, a lower cut as well, or none?
   What sieves or classifiers, what PSD did they print or characterize, and what fraction was below 20 um?
3. Commercial LPBF Al powder specifications (EOS, Nikon SLM Solutions, Renishaw, Aconity, AP&C, Carpenter
   Additive, Valimet, ECKART, Toyal, IMR, Elementum): stated size range and how much material below 15 or
   20 um they allow (D10 limits, maximum percent below a size). What PSD and layer thickness do Aconity MIDI
   or AconityMINI users report for AlSi10Mg?
4. For research builds (single tracks, density cubes, a few tensile bars) on a research LPBF machine, with
   2 % by number and under 1 % by volume below 20 um, is printing without a lower cut defensible? What would a
   reviewer expect to see reported instead (PSD by laser diffraction or image analysis, flow and density
   measurements)? Under what conditions would the fines matter (e.g. thin layers, recycled powder, humid
   storage)?
5. Safety: how explosibility of aluminium dust (minimum ignition energy, Kst, minimum explosible
   concentration) depends on particle size between 10 and 60 um, and whether removing the fines changes the
   handling precautions (NFPA 484) for the remaining powder.

Finish with a short recommendation: lower cut or not for test builds, at what size, and what measurement
would change the answer.

```

</details>

Question: Context. A university lab ultrasonically atomizes aluminium alloys (Al 4047 / AlSi12 and 6063) on an
AMAZEMET rePOWDER (about 40 kHz, molybdenum plate) in 100-250 g runs, for laser powder bed fusion on an
Aconity MIDI. The powder is highly spherical. An SEM image-analysis PSD of a nickel-aluminium bronze from the
same atomizer (5,937 particles) gave number D10/D50/D90 of 35/47/72 um and volume D10/D50/D90 of
46/104/209 um, with 2.1 % by number and under 0.1 % by volume below 20 um. A first SEM look at the Al lots
found the smallest particles mostly 40-60 um. The lab has 8 in (200 mm) stainless test sieves at 250 um
(No. 60) and 63 um (No. 230), with 45 um (No. 325) on order, and no sieve shaker yet. The runs plan targets a
15-45 um window; an earlier plan targeted 20-63 um.

Question: does the sub-15/20 um fraction matter for LPBF of aluminium alloys, and is "no lower cut" defensible?
Use experimental papers and give numbers with sources.

1. Measured effects of fines (below 15-20 um) in Al alloy LPBF powders (AlSi10Mg, AlSi12, AlSi7Mg, 4047,
   6061/6063, Scalmalloy) on flowability (Hall/Carney flow, avalanche angle, revolution powder analysis,
   Hausner ratio, FT4 cohesion), spreadability and layer quality (blade, roller, brush or rubber recoaters),
   packing density, spatter and denudation, porosity (lack of fusion, keyhole), surface roughness, powder
   oxygen and hydrogen, and tensile properties. Which studies varied the fines content of one Al powder
   (blended fines, 0-63 vs 20-63 vs 15-45 um, or recycled powder that lost its fines), and what fines fraction
   (by volume and by number) changed the outcome? Explain the cohesion argument (granular Bond number,
   van der Waals versus weight) for Al at its low density, at 10, 20 and 45 um.
2. What do LPBF and powder papers on ultrasonically atomized powders (Al especially; AMAZEMET rePOWDER, ATO
   Lab/Lab+, other ultrasonic atomizers; e.g. Yankin 2025, Priyadarshi 2024, Ukabhai 2025, Balasz 2023/2024,
   Hinrichs 2021, Zrodowski, Pilarski, Kaminski) actually do: an upper cut only, a lower cut as well, or none?
   What sieves or classifiers, what PSD did they print or characterize, and what fraction was below 20 um?
3. Commercial LPBF Al powder specifications (EOS, Nikon SLM Solutions, Renishaw, Aconity, AP&C, Carpenter
   Additive, Valimet, ECKART, Toyal, IMR, Elementum): stated size range and how much material below 15 or
   20 um they allow (D10 limits, maximum percent below a size). What PSD and layer thickness do Aconity MIDI
   or AconityMINI users report for AlSi10Mg?
4. For research builds (single tracks, density cubes, a few tensile bars) on a research LPBF machine, with
   2 % by number and under 1 % by volume below 20 um, is printing without a lower cut defensible? What would a
   reviewer expect to see reported instead (PSD by laser diffraction or image analysis, flow and density
   measurements)? Under what conditions would the fines matter (e.g. thin layers, recycled powder, humid
   storage)?
5. Safety: how explosibility of aluminium dust (minimum ignition energy, Kst, minimum explosible
   concentration) depends on particle size between 10 and 60 um, and whether removing the fines changes the
   handling precautions (NFPA 484) for the remaining powder.

Finish with a short recommendation: lower cut or not for test builds, at what size, and what measurement
would change the answer.


## Does the Sub-15/20 μm Fraction Matter for LPBF of Aluminium Alloys, and Is "No Lower Cut" Defensible?

### 1. Measured Effects of Fines (<15–20 μm) in Al Alloy LPBF Powders

**Flowability and cohesion.** Fine aluminium particles increase interparticle cohesion, specific energy, and basic flow energy, impairing low-stress powder flow (batistao2026surfacefunctionalizationof pages 90-94, batistao2026surfacefunctionalizationof pages 103-106). For AA2017 aluminium alloy powder, untreated gas-atomized powder with a broad PSD showed no measurable Carney funnel flow, while surface-modified powders with controlled fines showed improved flow (batistao2026surfacefunctionalizationof pages 94-100). The low density of aluminium (ρ ≈ 2670 kg/m³) is specifically identified as a factor that increases the relative importance of adhesion and van der Waals forces compared to gravitational forces, making Al powders particularly susceptible to poor flow at fine particle sizes (batistao2026surfacefunctionalizationof pages 94-100). Recycling studies on AlSi10Mg and AlSi7Mg consistently show that loss of fines during reuse *improves* flowability: avalanche angle decreases and cohesion drops (weiss2022ontheinfluence pages 4-5, warner2026theinfluenceof pages 4-5), confirming that fines are a flowability liability.

**The cohesion argument (granular Bond number).** The granular Bond number BN = F_i/F_g, where F_i is the interparticle attractive force (dominated 80–90% by van der Waals forces) and F_g is gravitational force, determines whether a powder behaves cohesively (zrodowski2021novelcoldcrucible pages 1-3). For particles below approximately 100 μm, surface forces become comparable to weight (astarita2026powderspreadingand pages 9-12). The van der Waals force between two equal spheres scales as F_vdW ∝ d (via the Hamaker constant A and contact separation z₀: F = Ad/(24z₀²)), while gravitational force scales as F_g ∝ ρd³. Their ratio BN ∝ 1/(ρd²), meaning BN increases sharply as particle size decreases and as density decreases. For aluminium (ρ ≈ 2.7 g/cm³) versus steel (ρ ≈ 7.9 g/cm³), the Bond number at a given particle size is roughly 3× higher for Al. Taking typical values (A ≈ 3×10⁻¹⁹ J for Al₂O₃-coated surfaces, z₀ ≈ 0.4 nm), BN ≈ 1 occurs near d ≈ 50–70 μm for Al (versus ~30–40 μm for steel). At 20 μm, BN is roughly 6–10 for Al; at 10 μm, BN is roughly 25–40 — firmly in the cohesive regime. At 45 μm, BN is near unity. This means aluminium particles below ~20 μm are strongly cohesive and will significantly impair free-surface powder flow and spreading uniformity, more so than the same-sized steel particles (zrodowski2021novelcoldcrucible pages 1-3, astarita2026powderspreadingand pages 7-9).

**Packing density and layer quality.** Solyaev et al. (2026) sieved a commercial AlSi10Mg powder into five fractions and measured both volumetric and thin-layer packing density. The finest fraction P1 (d50 = 25.8 μm volume / 28.1 μm layer, d10 = 17.2 μm) had the *lowest* thin-layer packing density (0.380), compared to 0.432 for the standard powder P0 (d50 = 48.4 μm) and 0.508 for the coarsest fraction P5 (d50 = 65.9 μm). Finer powders pack less efficiently in thin layers relevant to LPBF (solyaev2026ontheinfluence pages 6-8). This directly demonstrates that while fine particles can fill interstices in bulk, in thin-layer spreading they agglomerate and leave gaps.

**Absorptivity and single-track formation.** Despite their poorer packing, fine AlSi10Mg powders showed significantly higher effective absorptivity. In the Solyaev et al. study, the finest fraction P1 had the smallest lack-of-fusion zone — almost all single tracks were fully fused — while the coarsest fraction P5 had the largest lack-of-fusion zone. The absorptivity increases for finer powders because the ratio of layer thickness to particle size (h/d) increases, promoting more multiple reflections. This advantage is most pronounced at low energy densities (solyaev2026ontheinfluence pages 3-6, solyaev2026ontheinfluence pages 14-15).

**Porosity and mechanical properties.** The Solyaev study focused on single tracks rather than bulk density cubes, so direct porosity data for the fractions is not reported. However, recycling studies provide indirect evidence: Cordova et al. (2020) found that Al-Mg-Sc-Zr powder with reduced fines after reuse produced higher porosity (0.15% vs. 0.06% for virgin), with more 10–30 μm pores attributed to lower packing density (cordova2020effectsofpowder pages 19-22). Conversely, Weiss et al. (2022) found that AlSi10Mg powder that coarsened during 10 recycling cycles maintained >99% relative density and actually showed improved tensile properties (+7–17% yield strength), attributed to improved powder flow and packing uniformity (weiss2022ontheinfluence pages 9-10, weiss2022ontheinfluence pages 4-5). Warner et al. (2026) found AlSi7Mg maintained 99.2–99.3% relative density through 10 reuse cycles despite progressive loss of fines (warner2026theinfluenceof pages 5-7). The evidence suggests that moderate fines content (<2–3% by volume below 20 μm) does not significantly harm bulk density when process parameters are optimized, but excessive fines can degrade layer uniformity.

**Oxygen and hydrogen.** Fine particles have higher specific surface area and proportionally more surface oxide. Recycling studies show oxygen content increases with reuse, though this is partly from environmental exposure rather than fines content per se (raza2021degradationofalsi10mg pages 3-4, lopes2026recyclabilityinmetal pages 9-11).

### 2. Ultrasonically Atomized Powders: What PSD Cuts Are Used?

Ultrasonic atomization at ~35–40 kHz naturally produces a relatively narrow PSD centered around 40–55 μm, with limited material below 20 μm. Published studies show:

- **Grzelak et al. (2022)** — ATO system, 316L steel, 35 kHz: classified to **20–63 μm** by sieve shaker (DIN 66165-1, Multiserw LPzE-3e, 50 Hz). Before classification, 92.3% of UA powder was already within 20–63 μm. Median ~44 μm. Both upper and lower cuts applied (grzelak2022acomparativestudy pages 6-8, grzelak2022acomparativestudy pages 2-4).

- **Bałasz et al. (2023)** — UA Ti6Al4V, classified to **63 ± 20 μm** (i.e., approximately 43–83 μm), sieve shaker per DIN 66165-1. PSD: D10 = 40.2, D50 = 52.0, D90 = 60.8 μm (number). Lower cut applied (scientific2023comparisonofultrasonic pages 7-8).

- **Bashmakova et al. (2026)** — ATO Lab Plus, 316L from printed rods: sieved through **53 μm mesh** (upper cut only). After sieving, D10 = 12–15 μm, D50 = 31–34 μm, D90 ≈ 49 μm. No explicit lower cut; sub-20 μm fraction not reported but D10 values of 12–15 μm imply ~10% volume below ~15 μm (bashmakova2026ontheultrasonic pages 7-9, bashmakova2026ontheultrasonic pages 9-11, bashmakova2026ontheultrasonic pages 5-7).

- **Yankin et al. (2025)** — AlSi12, UA: sieved through **63 μm mesh** only (upper cut). ~75% of powder was usable (<63 μm). D10 = 38.7–44.7, D50 = 52.3–54.7, D90 = 66.4–72.7 μm. Span 0.40–0.64. With D10 ≈ 39–45 μm, very little material below 20 μm (yankin2025effectofultrasonic pages 3-4, yankin2025effectofultrasonic pages 2-3).

- **Ge et al. (2025)** — rePOWDER (AMAZEMET), Al-Zr-Er-Ni alloy: Q10 = 33.6, Q50 = 52.3, Q90 = 91.1 μm. No explicit sieving/classification mentioned beyond dynamic image analysis. With Q10 = 33.6 μm, negligible material below 20 μm. Achieved >99.95% printing density (ge2025highstrengthadditivelymanufacturable pages 4-6, ge2025highstrengthadditivelymanufacturable pages 8-9).

- **Żrodowski et al. (2021)** — Cold crucible UA, 20 kHz: tested various alloys. Powder output suitable for AM reached up to 60% below 50 μm. The sub-50 μm fraction was generally the target for LPBF (zrodowski2021novelcoldcrucible pages 6-8).

**Summary:** Most UA studies apply an upper cut (53–63 μm). Some also apply a lower cut at 20 μm (Grzelak, Bałasz). When no lower cut is applied, the inherently narrow PSD of UA at 35–40 kHz (D10 typically 35–45 μm for Al alloys) means very little material is below 20 μm naturally. The user's NiAlBz SEM data (D10 number = 35 μm, <0.1% by volume below 20 μm) is consistent with this.

### 3. Commercial LPBF Al Powder Specifications

Published powder specifications for commercial LPBF aluminium powders include:

- **SLM Solutions (now Nikon SLM Solutions):** AlSi10Mg specified as **20–63 μm** (pal2022linkingpowderproperties pages 2-4).
- **EOS:** AlSi10Mg specified as **25–70 μm** (pal2022linkingpowderproperties pages 2-4). The higher D10 floor (25 μm) implicitly limits fines below 20 μm.
- **Standard LPBF practice:** The 20–63 μm range is the most commonly referenced in literature for Al alloys (arias2024tailoringthecomposition pages 60-66, grzelak2022acomparativestudy pages 6-8).

Typical commercial AlSi10Mg powders from gas atomization report D10 values of 20–30 μm (volume-weighted), with virgin powder D10 ≈ 18–27 μm depending on supplier (weiss2022ontheinfluence pages 4-5, warner2026theinfluenceof pages 4-5). The lower size limit in commercial specs (20 or 25 μm) serves primarily to exclude the cohesive fine fraction. Detailed fines limits (e.g., "maximum X% below 15 μm") are not commonly published in open literature but are typically controlled through the D10 floor — a D10 of 20 μm implies roughly 10% of volume is below 20 μm, while a D10 of 25 μm implies less than 10%.

### 4. Defensibility of "No Lower Cut" for Research Builds

For the specific conditions described — ultrasonically atomized Al 4047/6063 at ~40 kHz, with SEM-derived D10 (number) ≈ 35–40 μm, <0.1% by volume and ~2% by number below 20 μm — **printing without a lower sieve cut is defensible for research builds**, for the following reasons:

1. **The fines fraction is negligibly small.** At <0.1% by volume below 20 μm, the amount of potentially cohesive material is far below any threshold shown to affect outcomes in the literature.

2. **UA naturally produces a narrow PSD with few fines.** Unlike gas atomization (which produces a log-normal distribution extending well below 10 μm), ultrasonic atomization at 40 kHz produces particles governed by capillary wave physics, yielding D50 ≈ 45–55 μm with limited fine tails (yankin2025effectofultrasonic pages 3-4, solyaev2026ontheinfluence pages 3-6).

3. **Multiple UA-LPBF studies used only an upper cut** without adverse consequences (Yankin: 63 μm only; Bashmakova: 53 μm only; Ge/rePOWDER: no explicit cut, >99.95% density).

**What a reviewer would expect to see reported:**
- PSD by laser diffraction (ISO 13320) or dynamic image analysis (ISO 13322), reporting D10/D50/D90 and span, ideally both number- and volume-weighted
- Confirmation that the sub-20 μm fraction is small (<1% by volume)
- Hall or Carney flow time (ASTM B213/B964), or avalanche angle / revolution powder analysis
- Apparent and tap density (ASTM B212/B527) or Hausner ratio
- SEM images of powder morphology
- Oxygen content of powder

**Conditions where fines would matter:**
- **Thin layers (<30 μm):** Layer thickness approaching individual particle diameter amplifies the effect of cohesive fines on spreading uniformity (astarita2026powderspreadingand pages 9-12, solyaev2026ontheinfluence pages 6-8)
- **Recycled powder accumulating moisture:** Capillary bridges from humidity add to van der Waals cohesion; Al's oxide layer is hygroscopic
- **Significantly different atomization conditions** that shift the PSD to finer sizes (e.g., higher frequency, different alloy viscosity)
- **Blade/rubber recoaters** more sensitive to cohesive agglomerates than roller recoaters

### 5. Safety: Aluminium Dust Explosibility vs. Particle Size

Aluminium dust explosion parameters are strongly particle-size-dependent:

| Parameter | 40 μm Al | <10 μm Al (est.) | 100 nm Al |
|---|---|---|---|
| MIE (mJ) | 59.7 | <1 (extrapolated) | <1 |
| K_St (bar·m/s) | 77 (St-1) | ~200–400 | 296–349 (St-2/St-3) |
| MEC (g/m³) | 35 | ~40–50 | 40–50 |
| P_max (bar) | 5.9 | — | 7.3–12.5 |

Data from Wu et al. (2010) (wu2010explosioncharacteristicsof pages 2-4, wu2010explosioncharacteristicsof pages 1-2, wu2010explosioncharacteristicsof pages 4-5, wu2010explosioncharacteristicsof pages 5-5). Literature values for micron-scale aluminium by size band: MIE ≈ 8 mJ for 0–8 μm, 6 mJ for 8–20 μm, 14 mJ for 20–37 μm, and 48 mJ for >37 μm (wu2010explosioncharacteristicsof pages 1-2). MEC reportedly increases substantially above ~50 μm diameter, reaching 125 g/m³ at 52 μm and 250 g/m³ at 71 μm (wu2010explosioncharacteristicsof pages 2-4).

Fine aluminium can achieve K_St > 300 bar·m/s (St-3 classification, "extremely severe"), with MIE < 10 mJ indicating very high ignition sensitivity (taveau2019metaldustsexplosion pages 1-2). The K_St value can double in larger test vessels due to radiative heat transfer effects specific to aluminium (taveau2019metaldustsexplosion pages 1-2). Pure aluminium powder (d50 ≈ 29 μm) is listed with K_St = 415 bar·m/s and hazard classification St-3 (nalbocUnknownyearexperimentaldeterminationof pages 3-5).

**Does removing fines change handling precautions?** Removing the sub-20 μm fraction would modestly increase the MIE (from ~6–14 mJ to ~48–60 mJ for the remaining 20–60 μm powder) and reduce K_St from potentially St-2/St-3 to St-1 severity. However, even 40 μm aluminium powder remains highly explosible: MIE = 59.7 mJ is still orders of magnitude below common ignition sources, MEC = 35 g/m³ is very low, and P_max = 5.9 bar is significant. NFPA 484 requirements for combustible metal dust handling (inerting, grounding, housekeeping, explosion venting) apply regardless of whether the sub-20 μm fraction is present. **Removing fines does not eliminate the need for any NFPA 484 precaution** for a 20–60 μm aluminium powder — the powder remains a severe explosion hazard.

### Recommendation

**For research test builds (single tracks, density cubes, tensile bars) on the Aconity MIDI with ultrasonically atomized Al 4047 or 6063:**

1. **A lower sieve cut is not necessary** given the UA powder characteristics described. With D10 (number) ≈ 35–40 μm and <0.1% by volume below 20 μm, the fines fraction is negligible and well below any threshold shown to affect LPBF outcomes. Sieving at 63 μm (upper cut) is sufficient.

2. **If the 45 μm sieve arrives**, it can be used to narrow the PSD to the target 15–45 μm (or even 20–45 μm) window, but a lower cut at 15 or 20 μm will remove virtually no material from this UA powder — it would be effort without effect.

3. **What would change this answer:** If laser diffraction PSD reveals more than ~5% by volume below 20 μm (unlikely for 40 kHz UA of aluminium), or if avalanche-angle / revolution-powder-analysis testing shows cohesive behavior (avalanche angle >55°, surface fractal >5.0), then a lower cut at 20 μm would be warranted. A significant change in atomization parameters (lower amplitude, higher melt superheat) that shifts the PSD finer would also warrant reassessment.

4. **Minimum characterization for publication:** Report PSD by laser diffraction or calibrated image analysis (D10/D50/D90, span), apparent density, and at least one flow measurement. State explicitly that the sub-20 μm fraction is <0.1% by volume and that no lower sieve cut was applied, with justification.

5. **Safety is unchanged:** All NFPA 484 precautions for combustible aluminium powder (inert atmosphere, grounding, explosion-proof enclosures, minimizing dust accumulation) must be maintained regardless of whether fines are removed, as the 40–60 μm aluminium powder remains a severe explosion hazard (MIE ≈ 60 mJ, K_St ≈ 77 bar·m/s, MEC ≈ 35 g/m³).

References

1. (batistao2026surfacefunctionalizationof pages 90-94): BF Batistão. Surface functionalization of the aa2017 aluminum alloy powder for use in additive manufacturing. Unknown journal, 2026.

2. (batistao2026surfacefunctionalizationof pages 103-106): BF Batistão. Surface functionalization of the aa2017 aluminum alloy powder for use in additive manufacturing. Unknown journal, 2026.

3. (batistao2026surfacefunctionalizationof pages 94-100): BF Batistão. Surface functionalization of the aa2017 aluminum alloy powder for use in additive manufacturing. Unknown journal, 2026.

4. (weiss2022ontheinfluence pages 4-5): C. Weiss, C. L. Haefner, and J. Munk. On the influence of alsi10mg powder recycling behavior in the lpbf process and consequences for mechanical properties. JOM, 74:1188-1199, Jan 2022. URL: https://doi.org/10.1007/s11837-021-05080-4, doi:10.1007/s11837-021-05080-4. This article has 41 citations and is from a peer-reviewed journal.

5. (warner2026theinfluenceof pages 4-5): James H. Warner, Simon P. Ringer, and Gwénaëlle Proust. The influence of powder reuse on alsi7mg manufactured by laser powder bed fusion. Progress in Additive Manufacturing, 11:6191-6208, May 2026. URL: https://doi.org/10.1007/s40964-026-01699-4, doi:10.1007/s40964-026-01699-4. This article has 2 citations and is from a peer-reviewed journal.

6. (zrodowski2021novelcoldcrucible pages 1-3): Łukasz Żrodowski, Rafał Wróblewski, Tomasz Choma, Bartosz Morończyk, Mateusz Ostrysz, Marcin Leonowicz, Wojciech Łacisz, Piotr Błyskun, Jan S. Wróbel, Grzegorz Cieślak, Bartłomiej Wysocki, Cezary Żrodowski, and Karolina Pomian. Novel cold crucible ultrasonic atomization powder production method for 3d printing. Materials, 14:2541, May 2021. URL: https://doi.org/10.3390/ma14102541, doi:10.3390/ma14102541. This article has 70 citations.

7. (astarita2026powderspreadingand pages 9-12): A. Astarita. Powder spreading and layer deposition in metal powder bed fusion. ArXiv, Jun 2026. URL: https://doi.org/10.48550/arxiv.2606.22989, doi:10.48550/arxiv.2606.22989. This article has 0 citations.

8. (astarita2026powderspreadingand pages 7-9): A. Astarita. Powder spreading and layer deposition in metal powder bed fusion. ArXiv, Jun 2026. URL: https://doi.org/10.48550/arxiv.2606.22989, doi:10.48550/arxiv.2606.22989. This article has 0 citations.

9. (solyaev2026ontheinfluence pages 6-8): Y. Solyaev, V. Dobryanskiy, Nguyen Long, and Stanislav Chernyshikhin. On the influence of powder particle size on single-track formation in laser powder bed fusion of alsi10mg alloy. Continuum Mechanics and Thermodynamics, Jul 2026. URL: https://doi.org/10.1007/s00161-026-01516-x, doi:10.1007/s00161-026-01516-x. This article has 1 citations and is from a peer-reviewed journal.

10. (solyaev2026ontheinfluence pages 3-6): Y. Solyaev, V. Dobryanskiy, Nguyen Long, and Stanislav Chernyshikhin. On the influence of powder particle size on single-track formation in laser powder bed fusion of alsi10mg alloy. Continuum Mechanics and Thermodynamics, Jul 2026. URL: https://doi.org/10.1007/s00161-026-01516-x, doi:10.1007/s00161-026-01516-x. This article has 1 citations and is from a peer-reviewed journal.

11. (solyaev2026ontheinfluence pages 14-15): Y. Solyaev, V. Dobryanskiy, Nguyen Long, and Stanislav Chernyshikhin. On the influence of powder particle size on single-track formation in laser powder bed fusion of alsi10mg alloy. Continuum Mechanics and Thermodynamics, Jul 2026. URL: https://doi.org/10.1007/s00161-026-01516-x, doi:10.1007/s00161-026-01516-x. This article has 1 citations and is from a peer-reviewed journal.

12. (cordova2020effectsofpowder pages 19-22): Laura Cordova, Ton Bor, Marc de Smit, Simone Carmignato, Mónica Campos, and Tiedo Tinga. Effects of powder reuse on the microstructure and mechanical behaviour of al–mg–sc–zr alloy processed by laser powder bed fusion (lpbf). Additive Manufacturing, 36:101625, Dec 2020. URL: https://doi.org/10.1016/j.addma.2020.101625, doi:10.1016/j.addma.2020.101625. This article has 165 citations and is from a highest quality peer-reviewed journal.

13. (weiss2022ontheinfluence pages 9-10): C. Weiss, C. L. Haefner, and J. Munk. On the influence of alsi10mg powder recycling behavior in the lpbf process and consequences for mechanical properties. JOM, 74:1188-1199, Jan 2022. URL: https://doi.org/10.1007/s11837-021-05080-4, doi:10.1007/s11837-021-05080-4. This article has 41 citations and is from a peer-reviewed journal.

14. (warner2026theinfluenceof pages 5-7): James H. Warner, Simon P. Ringer, and Gwénaëlle Proust. The influence of powder reuse on alsi7mg manufactured by laser powder bed fusion. Progress in Additive Manufacturing, 11:6191-6208, May 2026. URL: https://doi.org/10.1007/s40964-026-01699-4, doi:10.1007/s40964-026-01699-4. This article has 2 citations and is from a peer-reviewed journal.

15. (raza2021degradationofalsi10mg pages 3-4): Ahmad Raza, Tobias Fiegl, Imran Hanif, Andreas MarkstrÖm, Martin Franke, Carolin Körner, and Eduard Hryha. Degradation of alsi10mg powder during laser based powder bed fusion processing. Materials & Design, 198:109358, Jan 2021. URL: https://doi.org/10.1016/j.matdes.2020.109358, doi:10.1016/j.matdes.2020.109358. This article has 96 citations and is from a highest quality peer-reviewed journal.

16. (lopes2026recyclabilityinmetal pages 9-11): Ana Catarina Lopes, André F. V. Pedroso, Francisco J. G. Silva, Raul D. S. G. Campilho, Naiara P. V. Sebbe, and Rúben D. F. S. Costa. Recyclability in metal additive manufacturing: bridging powder lifecycle, defect evolution and fatigue-critical reliability across slm and ebm. Machines, 14:761, Jul 2026. URL: https://doi.org/10.3390/machines14070761, doi:10.3390/machines14070761. This article has 1 citations.

17. (grzelak2022acomparativestudy pages 6-8): Krzysztof Grzelak, Marcin Bielecki, Janusz Kluczyński, Ireneusz Szachogłuchowicz, Lucjan Śnieżek, Janusz Torzewski, Jakub Łuszczek, Łukasz Słoboda, Marcin Wachowski, Zenon Komorek, Marcin Małek, and Justyna Zygmuntowicz. A comparative study on laser powder bed fusion of differently atomized 316l stainless steel. Materials, 15:4938, Jul 2022. URL: https://doi.org/10.3390/ma15144938, doi:10.3390/ma15144938. This article has 24 citations.

18. (grzelak2022acomparativestudy pages 2-4): Krzysztof Grzelak, Marcin Bielecki, Janusz Kluczyński, Ireneusz Szachogłuchowicz, Lucjan Śnieżek, Janusz Torzewski, Jakub Łuszczek, Łukasz Słoboda, Marcin Wachowski, Zenon Komorek, Marcin Małek, and Justyna Zygmuntowicz. A comparative study on laser powder bed fusion of differently atomized 316l stainless steel. Materials, 15:4938, Jul 2022. URL: https://doi.org/10.3390/ma15144938, doi:10.3390/ma15144938. This article has 24 citations.

19. (scientific2023comparisonofultrasonic pages 7-8): International Scientific, B. Bałasz, M. Bielecki, W. Gulbiński, and Ł. Słoboda. Comparison of ultrasonic and other atomization methods in metal powder production. Journal of Achievements in Materials and Manufacturing Engineering, 116:11-24, Jan 2023. URL: https://doi.org/10.5604/01.3001.0016.3393, doi:10.5604/01.3001.0016.3393. This article has 38 citations.

20. (bashmakova2026ontheultrasonic pages 7-9): Olga Bashmakova, Leonid Fedorenko, Andrey Vasilev, Boris Zotov, Andrey Urzhumtsev, Ali Kavousi Sisi, Maria Lyange, Ivan Pelevin, Mikhail Gilvitinov, Ksenia Petukhova, Ekaterina Zinovyeva, and Stanislav Chernyshikhin. On the ultrasonic atomization of ss316l parts manufactured via laser powder bed fusion for the closed-loop production. Journal of Manufacturing and Materials Processing, 10:93, Mar 2026. URL: https://doi.org/10.3390/jmmp10030093, doi:10.3390/jmmp10030093. This article has 0 citations.

21. (bashmakova2026ontheultrasonic pages 9-11): Olga Bashmakova, Leonid Fedorenko, Andrey Vasilev, Boris Zotov, Andrey Urzhumtsev, Ali Kavousi Sisi, Maria Lyange, Ivan Pelevin, Mikhail Gilvitinov, Ksenia Petukhova, Ekaterina Zinovyeva, and Stanislav Chernyshikhin. On the ultrasonic atomization of ss316l parts manufactured via laser powder bed fusion for the closed-loop production. Journal of Manufacturing and Materials Processing, 10:93, Mar 2026. URL: https://doi.org/10.3390/jmmp10030093, doi:10.3390/jmmp10030093. This article has 0 citations.

22. (bashmakova2026ontheultrasonic pages 5-7): Olga Bashmakova, Leonid Fedorenko, Andrey Vasilev, Boris Zotov, Andrey Urzhumtsev, Ali Kavousi Sisi, Maria Lyange, Ivan Pelevin, Mikhail Gilvitinov, Ksenia Petukhova, Ekaterina Zinovyeva, and Stanislav Chernyshikhin. On the ultrasonic atomization of ss316l parts manufactured via laser powder bed fusion for the closed-loop production. Journal of Manufacturing and Materials Processing, 10:93, Mar 2026. URL: https://doi.org/10.3390/jmmp10030093, doi:10.3390/jmmp10030093. This article has 0 citations.

23. (yankin2025effectofultrasonic pages 3-4): Andrei Yankin, Hussain Ali Murtaza, Boris Golman, Asma Perveen, and Didier Talamona. Effect of ultrasonic atomization parameters on alsi12 aluminum powder characteristics for additive manufacturing. Scientific Reports, Jul 2025. URL: https://doi.org/10.1038/s41598-025-06086-7, doi:10.1038/s41598-025-06086-7. This article has 5 citations and is from a peer-reviewed journal.

24. (yankin2025effectofultrasonic pages 2-3): Andrei Yankin, Hussain Ali Murtaza, Boris Golman, Asma Perveen, and Didier Talamona. Effect of ultrasonic atomization parameters on alsi12 aluminum powder characteristics for additive manufacturing. Scientific Reports, Jul 2025. URL: https://doi.org/10.1038/s41598-025-06086-7, doi:10.1038/s41598-025-06086-7. This article has 5 citations and is from a peer-reviewed journal.

25. (ge2025highstrengthadditivelymanufacturable pages 4-6): Zhaoxuan Ge, Shaolou Wei, Zehua Liu, Tomasz Choma, Lukasz Zrodowski, Marc De Graef, A. John Hart, and S. Mohadeseh Taheri-Mousavi. High-strength additively manufacturable al-zr-er-ni alloys with high as-built ductility and thermal stability. May 2025. URL: https://doi.org/10.21203/rs.3.rs-6558867/v1, doi:10.21203/rs.3.rs-6558867/v1.

26. (ge2025highstrengthadditivelymanufacturable pages 8-9): Zhaoxuan Ge, Shaolou Wei, Zehua Liu, Tomasz Choma, Lukasz Zrodowski, Marc De Graef, A. John Hart, and S. Mohadeseh Taheri-Mousavi. High-strength additively manufacturable al-zr-er-ni alloys with high as-built ductility and thermal stability. May 2025. URL: https://doi.org/10.21203/rs.3.rs-6558867/v1, doi:10.21203/rs.3.rs-6558867/v1.

27. (zrodowski2021novelcoldcrucible pages 6-8): Łukasz Żrodowski, Rafał Wróblewski, Tomasz Choma, Bartosz Morończyk, Mateusz Ostrysz, Marcin Leonowicz, Wojciech Łacisz, Piotr Błyskun, Jan S. Wróbel, Grzegorz Cieślak, Bartłomiej Wysocki, Cezary Żrodowski, and Karolina Pomian. Novel cold crucible ultrasonic atomization powder production method for 3d printing. Materials, 14:2541, May 2021. URL: https://doi.org/10.3390/ma14102541, doi:10.3390/ma14102541. This article has 70 citations.

28. (pal2022linkingpowderproperties pages 2-4): Ritam Pal and Amrita Basak. Linking powder properties, printing parameters, post-processing methods, and fatigue properties in additive manufacturing of alsi10mg. Alloys, 1:149-179, Jul 2022. URL: https://doi.org/10.3390/alloys1020010, doi:10.3390/alloys1020010. This article has 46 citations.

29. (arias2024tailoringthecomposition pages 60-66): NR Arias. Tailoring the composition of the aa2017 to reduce its hot cracking susceptibility during lpbf. Unknown journal, 2024.

30. (wu2010explosioncharacteristicsof pages 2-4): Hong-Chun Wu, Hsin-Jung Ou, Hsiao-Chi Hsiao, and Tung-Sheng Shih. Explosion characteristics of aluminum nanopowders. Aerosol and Air Quality Research, 10:38-42, Feb 2010. URL: https://doi.org/10.4209/aaqr.2009.06.0043, doi:10.4209/aaqr.2009.06.0043. This article has 89 citations and is from a peer-reviewed journal.

31. (wu2010explosioncharacteristicsof pages 1-2): Hong-Chun Wu, Hsin-Jung Ou, Hsiao-Chi Hsiao, and Tung-Sheng Shih. Explosion characteristics of aluminum nanopowders. Aerosol and Air Quality Research, 10:38-42, Feb 2010. URL: https://doi.org/10.4209/aaqr.2009.06.0043, doi:10.4209/aaqr.2009.06.0043. This article has 89 citations and is from a peer-reviewed journal.

32. (wu2010explosioncharacteristicsof pages 4-5): Hong-Chun Wu, Hsin-Jung Ou, Hsiao-Chi Hsiao, and Tung-Sheng Shih. Explosion characteristics of aluminum nanopowders. Aerosol and Air Quality Research, 10:38-42, Feb 2010. URL: https://doi.org/10.4209/aaqr.2009.06.0043, doi:10.4209/aaqr.2009.06.0043. This article has 89 citations and is from a peer-reviewed journal.

33. (wu2010explosioncharacteristicsof pages 5-5): Hong-Chun Wu, Hsin-Jung Ou, Hsiao-Chi Hsiao, and Tung-Sheng Shih. Explosion characteristics of aluminum nanopowders. Aerosol and Air Quality Research, 10:38-42, Feb 2010. URL: https://doi.org/10.4209/aaqr.2009.06.0043, doi:10.4209/aaqr.2009.06.0043. This article has 89 citations and is from a peer-reviewed journal.

34. (taveau2019metaldustsexplosion pages 1-2): J. Taveau, S. Lemkowitz, S. Hochgreb, and D. Roekaerts. Metal dusts explosion hazards and protection. Chemical engineering transactions, 77:7-12, 2019. URL: https://doi.org/10.3303/cet1977002, doi:10.3303/cet1977002. This article has 24 citations and is from a peer-reviewed journal.

35. (nalbocUnknownyearexperimentaldeterminationof pages 3-5): I Nălboc, C Lupu, M Prodan, A Szolloşi-Moţa, and A Jurca. Experimental determination of explosion characteristics for aluminum powder derived from technological processes. Unknown journal, Unknown year.
