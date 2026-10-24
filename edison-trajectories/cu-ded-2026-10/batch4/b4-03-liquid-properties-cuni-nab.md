<!--
Edison Scientific LITERATURE task (batch 4)
- Task ID: ae462e78-bbfc-4fdd-b3b7-94d27225e306
- Submitted: 2026-10-17T06:11:10Z
- Fetched: 2026-10-17T06:41:51Z (status: success)
- Raw trajectory JSON: ../raw/b4-03-liquid-properties-cuni-nab.json.gz
- Synthesis: ../README.md
-->

Question:

CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Manufacturing Engineering, Brigham Young University; EXCLUDE the
PI's own publications) is writing an ONR FY2027 Young Investigator Program
proposal for the Materials & Processes for Additive Manufacturing program.
The work designs new pre-alloyed copper alloy powders for single-stream
blown-powder laser directed energy deposition (DED; one pre-alloyed powder
feed, not in-situ blending of elemental powders). Goals: deposits that are
dense and crack-free, both built on themselves and deposited on cast
nickel-aluminum bronze (NAB) and wrought Cu-Ni (repair), and that resist
seawater AS DEPOSITED (no post-build heat treatment) at least as well as
wrought 70-30 Cu-Ni (C71500). Alloy families: Cu-Ni (10-30 wt% Ni) with Fe,
Mn, Cr additions; aluminum bronzes / NAB with Ni, Fe, Mn. A secondary
objective is lower nickel content (nickel is a US critical mineral). Powder is
made in-house by ultrasonic atomization (AMAZEMET rePOWDER, induction
melting); size, Hall flow, apparent density and oxygen are measured per lot.
Method: the composition -> powder -> DED deposit -> microstructure ->
corrosion/hardness pipeline is a network of linked surrogate models searched
by cost-aware Bayesian optimization of function networks (cheap nodes such as
CALPHAD and short electrochemical tests are queried more often than expensive
ones such as 30-day immersion). ICME element: CALPHAD (Thermo-Calc) evaluated
along a heat-flow model of the DED thermal history, tested against
equilibrium-only CALPHAD and against no physics.

QUESTION: What measured liquid density, surface tension, and viscosity data
(vs temperature) exist for Cu-Ni alloys (10-30 wt% Ni, with Fe and Mn), for
Cu-Al and Cu-Al-Ni-Fe (aluminum bronze / NAB) melts, and for pure Cu?
Include electromagnetic levitation, sessile drop, and oscillating drop
results (e.g. Egry, Brillo, Schmitz), the effect of oxygen on Cu surface
tension, and models (Butler) for multicomponent melts. Using these, what
capillary-wave (Lang) droplet sizes follow at 20, 40 and 60 kHz for 90-10
Cu-Ni, 70-30 Cu-Ni and NAB at 50-100 C superheat, and how do they compare
with measured ultrasonic-atomized powder sizes for NAB (X50 about 98 um at
40 kHz) and other metals?

OUTPUT FORMAT: For each relevant item give the full citation with DOI, the
process (blown-powder laser DED / laser cladding / laser metal deposition,
wire-laser DED, wire-arc DED (WAAM), LPBF, cast, wrought), the alloy
composition in wt%, the test conditions (e.g. 3.5 wt% NaCl vs natural or
substitute seawater per ASTM D1141, duration, flow), and the key numbers
(porosity/density, corrosion current density or rate, Ecorr, impedance,
selective-attack depth, hardness, strength/elongation, powder size/flow/
oxygen). Tag each item: [CITE] worth citing; [NUMBERS] gives a quantitative
benchmark; [NAVY] Navy/DoD-funded or Navy application; [NOVELTY-RISK] overlaps
the proposed work (say how); [GAP] shows something not yet done. If the
literature does not answer part of the question, say so plainly instead of
padding with loosely related work. End with a ranked "Top 5 things the PI
should know" list.

---

Question: CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Manufacturing Engineering, Brigham Young University; EXCLUDE the
PI's own publications) is writing an ONR FY2027 Young Investigator Program
proposal for the Materials & Processes for Additive Manufacturing program.
The work designs new pre-alloyed copper alloy powders for single-stream
blown-powder laser directed energy deposition (DED; one pre-alloyed powder
feed, not in-situ blending of elemental powders). Goals: deposits that are
dense and crack-free, both built on themselves and deposited on cast
nickel-aluminum bronze (NAB) and wrought Cu-Ni (repair), and that resist
seawater AS DEPOSITED (no post-build heat treatment) at least as well as
wrought 70-30 Cu-Ni (C71500). Alloy families: Cu-Ni (10-30 wt% Ni) with Fe,
Mn, Cr additions; aluminum bronzes / NAB with Ni, Fe, Mn. A secondary
objective is lower nickel content (nickel is a US critical mineral). Powder is
made in-house by ultrasonic atomization (AMAZEMET rePOWDER, induction
melting); size, Hall flow, apparent density and oxygen are measured per lot.
Method: the composition -> powder -> DED deposit -> microstructure ->
corrosion/hardness pipeline is a network of linked surrogate models searched
by cost-aware Bayesian optimization of function networks (cheap nodes such as
CALPHAD and short electrochemical tests are queried more often than expensive
ones such as 30-day immersion). ICME element: CALPHAD (Thermo-Calc) evaluated
along a heat-flow model of the DED thermal history, tested against
equilibrium-only CALPHAD and against no physics.

QUESTION: What measured liquid density, surface tension, and viscosity data
(vs temperature) exist for Cu-Ni alloys (10-30 wt% Ni, with Fe and Mn), for
Cu-Al and Cu-Al-Ni-Fe (aluminum bronze / NAB) melts, and for pure Cu?
Include electromagnetic levitation, sessile drop, and oscillating drop
results (e.g. Egry, Brillo, Schmitz), the effect of oxygen on Cu surface
tension, and models (Butler) for multicomponent melts. Using these, what
capillary-wave (Lang) droplet sizes follow at 20, 40 and 60 kHz for 90-10
Cu-Ni, 70-30 Cu-Ni and NAB at 50-100 C superheat, and how do they compare
with measured ultrasonic-atomized powder sizes for NAB (X50 about 98 um at
40 kHz) and other metals?

OUTPUT FORMAT: For each relevant item give the full citation with DOI, the
process (blown-powder laser DED / laser cladding / laser metal deposition,
wire-laser DED, wire-arc DED (WAAM), LPBF, cast, wrought), the alloy
composition in wt%, the test conditions (e.g. 3.5 wt% NaCl vs natural or
substitute seawater per ASTM D1141, duration, flow), and the key numbers
(porosity/density, corrosion current density or rate, Ecorr, impedance,
selective-attack depth, hardness, strength/elongation, powder size/flow/
oxygen). Tag each item: [CITE] worth citing; [NUMBERS] gives a quantitative
benchmark; [NAVY] Navy/DoD-funded or Navy application; [NOVELTY-RISK] overlaps
the proposed work (say how); [GAP] shows something not yet done. If the
literature does not answer part of the question, say so plainly instead of
padding with loosely related work. End with a ranked "Top 5 things the PI
should know" list.


# Liquid properties and ultrasonic atomization of marine copper alloys

**Scope and confidence.** The strongest directly measured inputs are liquid Cu–Ni density, Cu–Ni surface tension, Cu–Ni–Fe density and surface tension, and Cu-rich Al–Cu surface tension. I found **no verified temperature-dependent measurements of all three properties for the proposed Cu–Ni–Fe–Mn compositions or for a representative liquid Cu–Al–Ni–Fe–Mn nickel-aluminum bronze (NAB)**. Accordingly, the NAB droplet calculations below are explicitly *screening estimates*, not predictions validated against measured NAB melt properties. All compositions below are **wt% unless marked at%**. The cited thermophysical experiments test melts, not DED deposits; seawater exposure conditions do not apply to them. (brillo2022densityandsurface pages 1-6, brillo2022densityandsurface pages 6-11, brillo2003densitydeterminationof pages 9-13, schmitz2014surfacetensionof pages 3-7)

## Measured melt-property evidence

1. **J. Brillo and I. Egry, “Density Determination of Liquid Copper, Nickel, and Their Alloys,” *International Journal of Thermophysics* 24, 1155–1170 (2003), DOI: 10.1023/A:1025021521945.** **Process:** electromagnetically levitated liquid; optical-shadowgraph density measurement. **Compositions:** Cu–10, –20, and –40 wt% Ni, among others; these are measured *binary* compositions, without Fe or Mn. Their fitted relation is ρ(T)=ρL+ρT(T−TL), with T and TL in °C, ρ in g cm⁻³: pure Cu **7.90−0.000765(T−1084)**; Cu–10Ni **7.97−0.000795(T−1136)**; Cu–20Ni **8.09−0.000957(T−1200)**; Cu–40Ni **8.13−0.00103(T−1280)**. **Cu–30Ni is not a directly tabulated measurement**: interpolation across 20 and 40 wt% gives approximately 8.11 g cm⁻³ at its estimated liquidus, before allowing for superheat. This paper does *not* measure viscosity. **[CITE] [NUMBERS] [GAP]** (brillo2003densitydeterminationof pages 1-5, brillo2003densitydeterminationof pages 9-13)

2. **E. Gorges and I. Egry, “The Surface Tension of Copper-Nickel Alloys,” *Journal of Materials Science* 30, 2517–2520 (1995), DOI: 10.1007/BF00362127.** **Process:** electromagnetic levitation and oscillating-drop tensiometry, over binary Cu–Ni composition and both superheated and undercooled temperatures. Explicit examples include **Cu–10 wt% Ni** and **Cu–40 wt% Ni**. The measured composition dependence agrees better with a Butler/subregular-solution treatment, incorporating Cu surface enrichment, than with ideal mixing. Their stated pure-element inputs, **not measured alloy-specific constants**, are γCu=**1.296−0.000234(T−1356)** N m⁻¹ and γNi=**1.770−0.000330(T−1728)** N m⁻¹, T in K. The plots support Cu-rich Cu–Ni surface tensions of roughly **1.2–1.4 N m⁻¹**, but do not furnish a trustworthy tabulated γ(T) specifically for commercial Fe/Mn-bearing C70600 or C71500. **[CITE] [NUMBERS] [GAP]** (gorges1995thesurfacetension pages 1-2, gorges1995thesurfacetension pages 2-3, gorges1995thesurfacetension pages 3-4)

3. **J. Brillo, I. Egry, and T. Matsushita, “Density and Surface Tension of Liquid Ternary Ni–Cu–Fe Alloys,” *International Journal of Materials Research* 97, 28–34 (2006), DOI: 10.3139/ijmr-2006-0005.** **Process:** electromagnetic levitation with optical density measurement and oscillating-drop tensiometry; reducing He–8 vol% H₂ atmosphere. **Compositions:** experimental cuts include Ni₀.₄₍₁₋ₓ₎CuₓFe₀.₆₍₁₋ₓ₎ and NiₓCu₀.₂Fe₀.₈₋ₓ, **atomic fractions**, not the approximately Cu–70Ni–30Fe/Mn compositions of a marine Cu–Ni alloy. Density and tension each vary approximately linearly with temperature for individual samples. At **1800 K**, the fixed-**20 at% Cu** cut has γ≈**1.30–1.45 N m⁻¹**; for Cu fractions greater than approximately **13 at%**, the other cut approaches **1.2–1.3 N m⁻¹**. A substantial ternary excess-volume contribution means binary-density interpolation can fail even where a Butler surface-tension calculation using binary excess Gibbs energies works reasonably well. **Neither viscosity nor Mn effects were measured.** **[CITE] [NUMBERS] [GAP]** (brillo2022densityandsurface pages 1-6, brillo2022densityandsurface pages 6-11, brillo2022densityandsurface pages 11-25)

4. **J. Schmitz, J. Brillo, and I. Egry, “Surface Tension of Liquid Al-Cu and Wetting at the Cu/Sapphire Solid-Liquid Interface,” *European Physical Journal Special Topics* 223, 469–479 (2014), DOI: 10.1140/epjst/e2014-02103-5.** **Process:** levitated, oscillating drops for liquid γ; separate sessile-drop experiments measure **Cu/sapphire contact angle**, *not* the free-surface tension of NAB. **Compositions:** pure Cu and Al₁₀Cu₉₀, Al₁₇Cu₈₃, etc., **at%**, not wt%. For **Al₁₀Cu₉₀**—approximately **4.5 wt% Al**, considerably below typical ≈9–10 wt% Al bronze—the reported γ(T)=**1.35−0.00021(T−1347)** N m⁻¹, with T in K; for pure Cu, **1.31−0.00034(T−1358)** N m⁻¹. At 50–100 K superheat these give Al₁₀Cu₉₀ γ≈**1.340–1.329 N m⁻¹**. **These are measured Cu–Al results, not measured NAB results**; adding Ni, Fe and Mn could change both γ and its sensitivity to oxygen. The cropped source table verifies the reference temperatures and coefficients. **[CITE] [NUMBERS] [GAP]** (schmitz2014surfacetensionof pages 1-3, schmitz2014surfacetensionof pages 3-7, schmitz2014surfacetensionof media 02001ec8)

5. **Z.-i. Morita and A. Kasama, “Surface Tension of Liquid Copper in Dilute Oxygen Concentrations,” *Journal of the Japan Institute of Metals* 40, 787–795 (1976), DOI: 10.2320/jinstmet1952.40.8_787.** **Process:** oxygen-partial-pressure-controlled sessile-drop measurement of **pure Cu**, **1100, 1200, 1300 and 1400 °C**; dissolved O below **0.02 at%**. Even dilute oxygen lowers γ, particularly at lower temperature; increasing oxygen can change the apparent γ-versus-T slope **from negative to positive**. Thus, neither a clean-Cu γ fit nor a binary Butler fit should be treated as an oxygen-insensitive atomizer input. Note that a search index misdated this article as 2006; the article itself shows **1976**. **[CITE] [NUMBERS] [GAP]** (morita2006surfacetensionof pages 1-3, morita2006surfacetensionof pages 5-7)

6. **R. J. L. Andon, L. A. Chapman, A. P. Day, and K. C. Mills, *Viscosities of Liquid Metals and Commercial Alloys*, National Physical Laboratory report CMMT(A)167 (1999); DOI: none verified.** **Process:** damped oscillation of a *liquid-filled crucible*, **not** the free, oscillating-drop method used for γ. For **pure Cu**, the report recommends **log₁₀[η/(mPa·s)]=−0.279+1254/T**, T in K: approximately **4.4 mPa·s at 1358 K** and **3.9 mPa·s at 1458 K**. Its investigated alloys include Cu–Sn, **not Cu–Ni or NAB**. This is a useful viscosity baseline, not evidence that a Cu–Ni/NAB viscosity has been measured. **[CITE] [NUMBERS] [GAP]** (andon2000viscositiesofliquid pages 1-7, andon2000viscositiesofliquid pages 15-18)

**Model distinction.** Butler’s treatment solves surface and bulk compositions as distinct thermodynamic states using component γ, molar volumes and partial excess Gibbs energies; surface-segregating Cu can therefore make γ non-linear in composition. For Cu–Ni–Fe the reported γ was captured substantially better than density using binary thermodynamics alone; **extending the calculation to Cu–Ni–Fe–Mn or NAB requires assessed multicomponent thermodynamics and independent oxygen-controlled validation**. Viscosity is an additional input affecting atomization onset and flow, but it does **not** enter the simple Lang diameter expression. **[CITE] [GAP]** (brillo2022densityandsurface pages 1-6, brillo2022densityandsurface pages 11-25, schmitz2009surfacetensionof pages 1-2, presz2024ultrasonicatomizationas pages 6-7)

## Capillary-wave droplet estimates and powder reality

The Lang screening relation is **d=0.34[8πγ/(ρf²)]¹ᐟ³**, where *f* is sonotrode frequency in Hz, γ is liquid free-surface tension in N m⁻¹ and ρ is *liquid*, not solid or loose-powder, density in kg m⁻³. Its result is a characteristic **initial droplet mean**, **not necessarily the sieved powder’s X₅₀**. It predicts the frequency ratio **d₂₀:d₄₀:d₆₀=1.587:1:0.763** for otherwise identical conditions. Lang’s original bibliographic identification is R. J. Lang, “Ultrasonic Atomization of Liquids,” *Journal of the Acoustical Society of America* **34**, 6–8 (1962); **its DOI was not verified in the retrieved literature**. The formula and its device-dependent limitations are documented by **W. Presz, R. Szostak-Staropiętka, A. Dziubińska and K. Kołacz, “Ultrasonic Atomization as a Method for Testing Material Properties of Liquid Metals,” *Materials* 17, 6109 (2024), DOI: 10.3390/ma17246109.** **[CITE] [NUMBERS] [GAP]** (presz2024ultrasonicatomizationas pages 6-7, presz2024ultrasonicatomizationas pages 12-14)

| Alloy; explicitly assumed liquid inputs at 50–100 °C superheat | 20 kHz | 40 kHz | 60 kHz | Status |
|---|---:|---:|---:|---|
| **90Cu–10Ni**: measured density fit gives ρ≈**7.93–7.89 g cm⁻³**; take γ≈**1.30 N m⁻¹** | **≈75 µm** | **≈47 µm** | **≈36 µm** | Density measured for the *binary*; γ representative, not a commercial Fe/Mn-bearing melt measurement. |
| **70Cu–30Ni**: estimated ρ≈**8.0 g cm⁻³** at superheat; take γ≈**1.33 N m⁻¹** | **≈75 µm** | **≈47 µm** | **≈36 µm** | Both 30 wt% Ni density and its γ are approximated from neighboring measurements. |
| **NAB**, nominally Cu–10Al–5Ni–5Fe: engineering **ρ≈7.4 g cm⁻³**; γ≈**1.33–1.34 N m⁻¹** proxied from *binary Al₁₀Cu₉₀ at%* | **≈77 µm** | **≈49 µm** | **≈37 µm** | **Neither input was verified experimentally for liquid NAB.** |

Values are rounded calculations from the stated inputs; within these assumptions, moving from 50 to 100 °C superheat changes the listed droplet sizes much less than doubling sonotrode frequency. For a fixed 40-kHz Cu–Ni density near 8.0 g cm⁻³, an illustrative **1.27–1.35 N m⁻¹** γ interval changes d only approximately **46–48 µm**. The largest model risk is therefore not small numerical rounding, but **unknown NAB melt properties and atomizer-specific breakup/collection physics**. (brillo2003densitydeterminationof pages 9-13, schmitz2014surfacetensionof pages 3-7, presz2024ultrasonicatomizationas pages 6-7)

7. **E. Uhlmann, J. Polte, J. M. Fasselt, V. Müller, C. Klötzer-Freese, R. Kleba-Ehrhardt, M. Biegler and M. Rethmeier, “A Comparative Evaluation of Powder Characteristics of Recycled Material from Bronze Grinding Chips for Additive Manufacturing,” *Materials* 17, 3396 (2024), DOI: 10.3390/ma17143396.** **Process:** induction melting and **40-kHz ultrasonic atomization**, not a reported seawater corrosion trial. **Material:** ground cast-ship-propeller NAB, measured atomized powder approximately **75.16Cu–9.83Al–6.76Fe–5.91Ni–2.33Mn wt%** by EDX. At **1300 °C**, Ar grade 5.0, 1.5-bar delivery onto a carbon-fiber sonotrode and a **200-µm finishing sieve**, measured *area-equivalent* **X₁₀/X₅₀/X₉₀=48/98/174 µm**. Powder O≈**0.013 wt%**, mean aspect ratio **0.935**, **82%** of particles aspect ratio >0.9, Carney flow **8.62 s/150 g** under ASTM B964, and Hausner ratio **1.05**. The **98-µm X₅₀ is about twice the ≈49-µm 40-kHz Lang NAB proxy**, but these are different statistics and the sample was sieved. The paper documents atomized **NAB powder for powder-DED**, so neither ultrasonic atomization of NAB nor spherical NAB DED feedstock can credibly be claimed as wholly unprecedented. It reports **Carney, not Hall**, flow; substituting one measurement for the other would be incorrect. **[CITE] [NUMBERS] [NAVY: ship-propeller application, not verified US Navy funding] [NOVELTY-RISK: ultrasonic NAB powder and DED feedstock already demonstrated] [GAP: controlled melt-property and frequency-to-size calibration, composition-designed as-deposited repair/corrosion testing].** (uhlmann2024acomparativeevaluation pages 1-2, uhlmann2024acomparativeevaluation pages 4-6, uhlmann2024acomparativeevaluation pages 7-10, uhlmann2024acomparativeevaluation pages 6-7, uhlmann2024acomparativeevaluation pages 10-12, uhlmann2024acomparativeevaluation pages 12-13)

**Other-material checks, with process kept distinct:** **X. Yang, H. Li, D. Ren, H. Lan, X. Hu, Q. Wang and P. Yu, “Effects of Ultrasonic Atomization Parameters on the Properties of Sn-58Bi Powder and Its Application in Ultrasonic-Assisted Soldering,” preprint (2026), DOI: 10.21203/rs.3.rs-10615585/v1**, reports **35-kHz** induction-fed **Sn–58Bi wt%** powder with **D₅₀=65.5 µm** at 199 °C, approximately **60 °C superheat**, in Ar; it is **not** a copper-alloy calibration. **D. Halápi and L. Varga, “Ultrasonic Powder Atomization for Additive Manufacturing,” *International Journal of Engineering and Management Sciences* 8, 69–75 (2023), DOI: 10.21791/IJEMS.2023.2.8**, reports **1.4551 steel** ultrasonic-powder sieve fractions, notably **63.92% at 45–63 µm**, but these are binned percentages rather than a directly comparable X₅₀ under documented identical atomizer settings. Device amplitude, flow and collection can invalidate naive transfer of Lang’s 0.34 coefficient. **[CITE] [NUMBERS] [GAP]** (yang2026effectsofultrasonic pages 1-5, halapi2023ultrasonicpowderatomization pages 1-4, presz2024ultrasonicatomizationas pages 6-7)

## What the nearest deposition/corrosion studies actually establish

8. **J. Song, X. A. Jimenez, A. C. To and Y. Fu, “Microstructures and Corrosion Properties of Wire Arc Additive Manufactured Copper–Nickel Alloys,” *Materials* 17, 876 (2024), DOI: 10.3390/ma17040876.** **Process:** **wire-arc DED/WAAM**, **not blown-powder laser DED**. Feed wire **67.5Cu–30Ni–0.7Mn–0.55Fe wt%** was deposited onto **wrought C71500**, measured **68.046Cu–30.46Ni–0.73Mn–0.56Fe wt%**, with 75Ar/25He shielding and interpass **150–200 °C**. On polished specimens after **3 h in naturally aerated, room-temperature 3.5 wt% NaCl**, WAAM sample 6 (**8 m/min wire feed; 1000 mm/min travel; 3.85-mm track spacing**) gave fitted film resistance **1.40×10⁵ Ω (XY)** and **1.66×10⁵ Ω (YZ)** versus wrought **1.08×10⁵ and 1.18×10⁵ Ω**, respectively. EIS covered **100 kHz–10 mHz**, with subsequent cyclic polarization. Microscopy found **no detectable pores or macro/microcracks**, but did **not** establish a numerical ≥99% density; the WAAM microstructure segregated Ni and showed preferential interdendritic attack. The paper reports film resistance, *passive* current and breakdown-potential trends; the retrieved quantitative table does **not** justify inventing **i₍corr₎, E₍corr₎, 30-day corrosion rate or attack depth**. Its strongest build is promising, but **3 h in static NaCl is not 30 days of flowing natural/ASTM D1141 seawater**. **[CITE] [NUMBERS] [NAVY: marine application, funding not verified] [NOVELTY-RISK: as-built C71500-on-C71500 and comparison to wrought already demonstrated by WAAM] [GAP: single-prealloyed-powder laser DED plus long-term seawater].** (song2024microstructuresandcorrosion pages 1-2, song2024microstructuresandcorrosion pages 2-5, song2024microstructuresandcorrosion pages 10-13, song2024microstructuresandcorrosion pages 14-17)

9. **L. Zhao, B. Du, J. Yao, H. Chen, R. Ding and K. Li, “Microstructure and Mechanical Properties of Nickel-Aluminum Bronze Coating on 17-4PH Stainless Steel by Laser Cladding,” *Chinese Journal of Mechanical Engineering* 35, 140 (2022), DOI: 10.1186/s10033-022-00807-z.** **Process:** **blown-powder laser deposition/cladding**, but onto **17-4PH steel, not cast NAB or wrought Cu–Ni**. Pre-alloyed powder **Cu balance–10.80Al–4.73Ni–4.10Fe–0.025O wt%**; laser powers **1500–2400 W**, scan **1.2 m/min**, 1.7-mm hatch, one or four layers. Coatings had reported **204–266 HV0.2** and good interfacial bonding; the lowest-power condition exhibited local lack of fusion. Substrate dilution produced Fe-rich features, a warning against assessing a repair alloy solely as an undiluted coupon. **No matched seawater E₍corr₎, i₍corr₎ or 30-day immersion benchmark was established in the retrieved study.** **[CITE] [NUMBERS] [NAVY: propeller application, funding not verified] [NOVELTY-RISK: pre-alloyed NAB powder laser deposition already exists] [GAP: NAB/NAB and Cu–Ni/Cu–Ni repair interfaces plus as-deposited long-term corrosion].** (zhao2022microstructureandmechanical pages 2-4, zhao2022microstructureandmechanical pages 6-9)

## Ranked top 5 things the PI should know

1. **Frame the novelty narrowly.** Pre-alloyed NAB powder, ultrasonic NAB atomization and deposited marine Cu–Ni are each precedented; the defensible question is **composition-designed, single-stream blown-powder laser DED** that is crack-free on **both cast NAB and wrought Cu–Ni** and meets a **matched, as-deposited, long-duration C71500 seawater benchmark**. (uhlmann2024acomparativeevaluation pages 6-7, zhao2022microstructureandmechanical pages 2-4, song2024microstructuresandcorrosion pages 1-2)
2. **Measure or explicitly bound liquid NAB γ, ρ and η.** Binary Al–Cu γ is a valuable prior, not an NAB measurement; oxygen, Ni/Fe/Mn and ternary excess volume threaten unvalidated interpolation. Do not claim Lang has accurately predicted the NAB X₅₀: the available **98-µm observation is ≈2×** the ≈49-µm proxy. (schmitz2014surfacetensionof pages 3-7, brillo2022densityandsurface pages 1-6, uhlmann2024acomparativeevaluation pages 6-7, morita2006surfacetensionof pages 5-7)
3. **Make powder a measured intermediate, not merely a composition label.** The published NAB precedent already gives **X₁₀/X₅₀/X₉₀=48/98/174 µm**, **0.013 wt% O** and excellent **Carney** flow. Record each new lot’s actual PSD, O, apparent density and **Hall** flow separately; assess sonotrode contamination and sieve yield when optimizing. (uhlmann2024acomparativeevaluation pages 10-12, uhlmann2024acomparativeevaluation pages 6-7, uhlmann2024acomparativeevaluation pages 4-6)
4. **Do not equate short NaCl electrochemistry with seawater qualification.** The quantified favorable C71500 comparison is **WAAM after 3 h in 3.5 wt% NaCl**; pair short EIS/polarization with matched wrought C71500 and longer **natural or ASTM D1141 seawater** exposure, reporting duration, aeration/flow, attack depth and interface behavior. No verified source here establishes the proposed **30-day, as-deposited, powder-DED** acceptance result. (song2024microstructuresandcorrosion pages 2-5, song2024microstructuresandcorrosion pages 10-13)
5. **Separate physics and optimization claims.** Butler/CALPHAD γ and measured binary/ternary density provide testable cheap-node priors, while segregation, dilution, defects and long-term corrosion remain downstream measurements. **R. Astudillo and P. I. Frazier, “Bayesian Optimization of Function Networks,” *NeurIPS* (2021), DOI: 10.48550/arXiv.2112.15311**, establishes optimization using observed intermediate outputs, but its demonstrated algorithm by itself is **not evidence that independently querying cheap nodes at different costs has already been validated for this copper-alloy pipeline**. This difference is an important methodological distinction to make explicitly. **[CITE] [GAP]** (brillo2022densityandsurface pages 1-6, astudillo2021bayesianoptimizationof pages 1-2, song2024microstructuresandcorrosion pages 2-5)

**Unanswered quantitative items:** I did not verify alloy-specific liquid **viscosity(T)** for Cu–10–30Ni–Fe–Mn or NAB; direct liquid-NAB **density(T)** or **surface-tension(T)**; or a matched **30-day as-deposited laser-powder-DED versus wrought C71500** seawater dataset. I therefore report no fabricated i₍corr₎, E₍corr₎, selective-attack depth, tensile strength or elongation for those missing tests.

References

1. (brillo2022densityandsurface pages 1-6): J. Brillo, I. Egry, and T. Matsushita. Density and surface tension of liquid ternary ni–cu–fe alloys. International Journal of Materials Research, 97:28-34, Jan 2022. URL: https://doi.org/10.3139/ijmr-2006-0005, doi:10.3139/ijmr-2006-0005. This article has 68 citations and is from a peer-reviewed journal.

2. (brillo2022densityandsurface pages 6-11): J. Brillo, I. Egry, and T. Matsushita. Density and surface tension of liquid ternary ni–cu–fe alloys. International Journal of Materials Research, 97:28-34, Jan 2022. URL: https://doi.org/10.3139/ijmr-2006-0005, doi:10.3139/ijmr-2006-0005. This article has 68 citations and is from a peer-reviewed journal.

3. (brillo2003densitydeterminationof pages 9-13): J. Brillo and I. Egry. Density determination of liquid copper, nickel, and their alloys. International Journal of Thermophysics, 24:1155-1170, Jul 2003. URL: https://doi.org/10.1023/a:1025021521945, doi:10.1023/a:1025021521945. This article has 233 citations and is from a peer-reviewed journal.

4. (schmitz2014surfacetensionof pages 3-7): J. Schmitz, J. Brillo, and I. Egry. Surface tension of liquid al-cu and wetting at the cu/sapphire solid-liquid interface. The European Physical Journal Special Topics, 223:469-479, Feb 2014. URL: https://doi.org/10.1140/epjst/e2014-02103-5, doi:10.1140/epjst/e2014-02103-5. This article has 12 citations.

5. (brillo2003densitydeterminationof pages 1-5): J. Brillo and I. Egry. Density determination of liquid copper, nickel, and their alloys. International Journal of Thermophysics, 24:1155-1170, Jul 2003. URL: https://doi.org/10.1023/a:1025021521945, doi:10.1023/a:1025021521945. This article has 233 citations and is from a peer-reviewed journal.

6. (gorges1995thesurfacetension pages 1-2): E. Gorges and I. Egry. The surface tension of copper-nickel alloys. Journal of Materials Science, 30:2517-2520, May 1995. URL: https://doi.org/10.1007/bf00362127, doi:10.1007/bf00362127. This article has 22 citations and is from a peer-reviewed journal.

7. (gorges1995thesurfacetension pages 2-3): E. Gorges and I. Egry. The surface tension of copper-nickel alloys. Journal of Materials Science, 30:2517-2520, May 1995. URL: https://doi.org/10.1007/bf00362127, doi:10.1007/bf00362127. This article has 22 citations and is from a peer-reviewed journal.

8. (gorges1995thesurfacetension pages 3-4): E. Gorges and I. Egry. The surface tension of copper-nickel alloys. Journal of Materials Science, 30:2517-2520, May 1995. URL: https://doi.org/10.1007/bf00362127, doi:10.1007/bf00362127. This article has 22 citations and is from a peer-reviewed journal.

9. (brillo2022densityandsurface pages 11-25): J. Brillo, I. Egry, and T. Matsushita. Density and surface tension of liquid ternary ni–cu–fe alloys. International Journal of Materials Research, 97:28-34, Jan 2022. URL: https://doi.org/10.3139/ijmr-2006-0005, doi:10.3139/ijmr-2006-0005. This article has 68 citations and is from a peer-reviewed journal.

10. (schmitz2014surfacetensionof pages 1-3): J. Schmitz, J. Brillo, and I. Egry. Surface tension of liquid al-cu and wetting at the cu/sapphire solid-liquid interface. The European Physical Journal Special Topics, 223:469-479, Feb 2014. URL: https://doi.org/10.1140/epjst/e2014-02103-5, doi:10.1140/epjst/e2014-02103-5. This article has 12 citations.

11. (schmitz2014surfacetensionof media 02001ec8): J. Schmitz, J. Brillo, and I. Egry. Surface tension of liquid al-cu and wetting at the cu/sapphire solid-liquid interface. The European Physical Journal Special Topics, 223:469-479, Feb 2014. URL: https://doi.org/10.1140/epjst/e2014-02103-5, doi:10.1140/epjst/e2014-02103-5. This article has 12 citations.

12. (morita2006surfacetensionof pages 1-3): V Maria and E VASILESCU. Surface tension of liquid copper in dilute oxygen concentrations. Journal of The Japan Institute of Metals, 40:787-795, 2006. URL: https://doi.org/10.2320/jinstmet1952.40.8\_787, doi:10.2320/jinstmet1952.40.8\_787. This article has 24 citations and is from a peer-reviewed journal.

13. (morita2006surfacetensionof pages 5-7): V Maria and E VASILESCU. Surface tension of liquid copper in dilute oxygen concentrations. Journal of The Japan Institute of Metals, 40:787-795, 2006. URL: https://doi.org/10.2320/jinstmet1952.40.8\_787, doi:10.2320/jinstmet1952.40.8\_787. This article has 24 citations and is from a peer-reviewed journal.

14. (andon2000viscositiesofliquid pages 1-7): RJL Andon, L Chapman, A Day, and KC Mills. Viscosities of liquid metals and commercial alloys. Unknown journal, 2000.

15. (andon2000viscositiesofliquid pages 15-18): RJL Andon, L Chapman, A Day, and KC Mills. Viscosities of liquid metals and commercial alloys. Unknown journal, 2000.

16. (schmitz2009surfacetensionof pages 1-2): J Schmitz, J Brillo, I Egry, and R Schmid-Fetzer. Surface tension of liquid al-cu binary alloys. Unknown journal, 2009.

17. (presz2024ultrasonicatomizationas pages 6-7): Wojciech Presz, Rafał Szostak-Staropiętka, Anna Dziubińska, and Katarzyna Kołacz. Ultrasonic atomization as a method for testing material properties of liquid metals. Materials, 17:6109, Dec 2024. URL: https://doi.org/10.3390/ma17246109, doi:10.3390/ma17246109. This article has 7 citations.

18. (presz2024ultrasonicatomizationas pages 12-14): Wojciech Presz, Rafał Szostak-Staropiętka, Anna Dziubińska, and Katarzyna Kołacz. Ultrasonic atomization as a method for testing material properties of liquid metals. Materials, 17:6109, Dec 2024. URL: https://doi.org/10.3390/ma17246109, doi:10.3390/ma17246109. This article has 7 citations.

19. (uhlmann2024acomparativeevaluation pages 1-2): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

20. (uhlmann2024acomparativeevaluation pages 4-6): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

21. (uhlmann2024acomparativeevaluation pages 7-10): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

22. (uhlmann2024acomparativeevaluation pages 6-7): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

23. (uhlmann2024acomparativeevaluation pages 10-12): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

24. (uhlmann2024acomparativeevaluation pages 12-13): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

25. (yang2026effectsofultrasonic pages 1-5): Xiaofeng Yang, Haodi Li, Dingying Ren, Hao Lan, Xiaoqiang Hu, Qian Wang, and Peng Yu. Effects of ultrasonic atomization parameters on the properties of sn-58bi powder and its application in ultrasonic-assisted soldering. Unknown journal, Aug 2026. URL: https://doi.org/10.21203/rs.3.rs-10615585/v1, doi:10.21203/rs.3.rs-10615585/v1.

26. (halapi2023ultrasonicpowderatomization pages 1-4): David Halapi and László Varga. Ultrasonic powder atomization for additive manufacturing. International Journal of Engineering and Management Sciences, 8:69-75, Jun 2023. URL: https://doi.org/10.21791/ijems.2023.2.8., doi:10.21791/ijems.2023.2.8. This article has 6 citations.

27. (song2024microstructuresandcorrosion pages 1-2): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

28. (song2024microstructuresandcorrosion pages 2-5): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

29. (song2024microstructuresandcorrosion pages 10-13): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

30. (song2024microstructuresandcorrosion pages 14-17): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

31. (zhao2022microstructureandmechanical pages 2-4): Lu Zhao, Baorui Du, Jun Yao, Haitao Chen, Ruochen Ding, and Kailun Li. Microstructure and mechanical properties of nickel-aluminum bronze coating on 17-4ph stainless steel by laser cladding. Chinese Journal of Mechanical Engineering, 35:1-12, Nov 2022. URL: https://doi.org/10.1186/s10033-022-00807-z, doi:10.1186/s10033-022-00807-z. This article has 25 citations and is from a peer-reviewed journal.

32. (zhao2022microstructureandmechanical pages 6-9): Lu Zhao, Baorui Du, Jun Yao, Haitao Chen, Ruochen Ding, and Kailun Li. Microstructure and mechanical properties of nickel-aluminum bronze coating on 17-4ph stainless steel by laser cladding. Chinese Journal of Mechanical Engineering, 35:1-12, Nov 2022. URL: https://doi.org/10.1186/s10033-022-00807-z, doi:10.1186/s10033-022-00807-z. This article has 25 citations and is from a peer-reviewed journal.

33. (astudillo2021bayesianoptimizationof pages 1-2): Raul Astudillo and Peter I. Frazier. Bayesian optimization of function networks. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2112.15311, doi:10.48550/arxiv.2112.15311. This article has 84 citations.
