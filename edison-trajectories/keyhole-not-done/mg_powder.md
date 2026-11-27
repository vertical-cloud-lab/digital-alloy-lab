<!--
Edison Scientific LITERATURE_HIGH report: Mg evaporation from Al alloys under a laser, and powder-bed absorptance of Al alloys
Job: job-futurehouse-paperqa3-high (LITERATURE_HIGH)
Task ID: 224156e1-0ff3-41bd-ab4d-eb84e96679a8
Created: 2026-11-27T03:35:54.598199Z  Status: success
Retrieved with edison-client from GitHub Actions for issue #235.
Prompt: QUERIES['mg_powder'] in scripts/edison_keyhole_not_done.py
-->

Question: Context: we have written our own physics-based keyhole and melt-pool model for laser powder bed fusion (1070 nm fibre laser, Gaussian beam 1/e^2 radius 40-45 um, 75-400 W, 0.3-2.4 m/s) of AlSi10Mg and a hypereutectic Al-24.3Si-0.14Mg (wt%) blend. It uses Drude-Fresnel optics of the liquid from its measured electrical resistivity, a ray tracer for multiple reflections in the keyhole, an energy balance at a keyhole wall at the boiling point, and CALPHAD enthalpies. We are now adding Mg evaporation, a powder layer, a tilted keyhole whose shape comes from a point-by-point wall energy balance, and Marangoni melt flow, and we need sourced inputs. Question: (a) how is selective Mg evaporation from Al-Mg and Al-Si-Mg melts modelled and measured under laser welding and LPBF: the Mg activity coefficient in liquid Al, the Langmuir and Knudsen-layer flux, diffusion-limited depletion of Mg at the surface, and measured Mg loss (e.g. Zhao and DebRoy 2001 for Al 5182; Mg loss in LPBF AlSi10Mg and in Al 5xxx keyhole welding)? Does Mg vapour lower the keyhole wall temperature, and by how much? Give the diffusion coefficient of Mg in liquid Al with its source. (b) What absorptance has been measured or computed at 1.06-1.07 um for powder layers of AlSi10Mg, Al-Si or Al (integrating sphere, calorimetry, ray tracing such as Boley et al. 2015, radiation transfer such as Gusarov and Kruth 2005), and how does it depend on layer thickness, packing density and particle size? Give the extinction coefficient formula used for packed beds of opaque spheres and typical AlSi10Mg powder-layer packing densities. Give DOIs with table or figure numbers.

## Part (a): Selective Mg Evaporation from Al–Mg and Al–Si–Mg Melts

### 1. Mg Activity Coefficient in Liquid Al

The standard approach for modeling Mg evaporation from dilute Al–Mg melts uses Henry's law with an activity coefficient γ_Mg ≈ 0.88, so that the Mg activity is a_Mg = 0.88·x_Mg, where x_Mg is the Mg mole fraction in the liquid (zhao2001weldmetalcomposition pages 2-3, semenov2012modellingofbinary pages 3-6). This value was adopted in the foundational laser-welding evaporation model of Zhao and DebRoy (2001, DOI: 10.1007/s11663-001-0018-6) for AA5182, and was also used by Semenov et al. (2012, DOI: 10.1088/0965-0393/20/5/055009) for binary Al–Mg arc welding (semenov2012modellingofbinary pages 3-6). Moser et al. (1998, DOI: 10.1361/105497198770342733) measured Mg activities in liquid Al–Mg alloys from vapor-pressure (Knudsen effusion) and emf measurements over wide composition and temperature ranges (x_Mg = 0.00035–0.887, T = 722–1188 K), from which γ_Mg can be obtained as a_Mg/x_Mg (moser1998newthermodynamicdata pages 4-5, moser1998newthermodynamicdata pages 3-4). For concentrated or ternary Al–Si–Mg melts, γ_Mg should be recalculated from CALPHAD databases rather than using the dilute Henry's-law value.

### 2. Langmuir and Knudsen-Layer Evaporation Flux

Zhao and DebRoy (2001) decompose the total vapor flux of alloying element i into two contributions (their Eq. [15]):

J_i = J_{c,i} + J_{P,i}

**Concentration-gradient (diffusive/Langmuir-type) flux** J_{c,i}: driven by the difference between the equilibrium vapor concentration at the melt-pool surface and the (negligible) concentration in the shielding gas, via a mass-transfer coefficient K_{g,i} computed for a jet impinging on a flat surface (their Eq. [5]) (zhao2001weldmetalcomposition pages 2-3, zhao2001weldmetalcomposition pages 3-4).

**Pressure-gradient (convective/Knudsen-layer) flux** J_{P,i}: at surface temperatures exceeding the alloy boiling point, the vapor pressure exceeds atmospheric and a convective flow develops through the Knudsen layer. The total pressure-gradient flux is (Eq. [13]):

J_P = ρ_v · M · S

where ρ_v is the vapor density at the outer edge of the Knudsen layer, M is the Mach number, and S is the speed of sound in the vapor at the edge temperature T_v. The elemental flux is then (Eq. [14]):

J_{P,i} = a_i · (P_i° / P_l) · (M_i / M_v) · J_P

The Knudsen-layer jump conditions (Eqs. [6]–[8]) relating temperature, density, condensation factor, and velocity parameter m at the layer edge to the liquid-surface conditions are solved together with the Rankine–Hugoniot relation (Eq. [11]) to determine M and ρ_v (zhao2001weldmetalcomposition pages 4-5, zhao2001weldmetalcomposition pages 3-4). This framework follows Anisimov and Knight's treatment of the Knudsen layer as a gasdynamic discontinuity. Semenov et al. (2012) extended this to a full binary-mixture Knudsen-layer model and noted that the conventional Langmuir/Schrage formula substantially overestimates evaporation rates under welding conditions because it assumes free-molecular (vacuum) flow, which is inapplicable in the collisional regime (semenov2012modellingofbinary pages 6-9).

He et al. (2003, DOI: 10.1088/0022-3727/36/23/033) and Liu et al. (2017) applied the same J_i = J_{c,i} + J_{P,i} framework to stainless-steel keyhole welding, confirming its generality across alloy systems (liu2017compositionchangeof pages 3-5, he2003alloyingelementvaporization pages 2-3).

### 3. Diffusion-Limited Depletion of Mg at the Surface

In the Zhao and DebRoy (2001) conduction-mode model, the weld pool is assumed to be well-mixed by Marangoni convection (velocities ~1 m/s), so a uniform Mg concentration is maintained throughout the pool, updated iteratively via a mass balance (their Eq. [17]) (zhao2001weldmetalcomposition pages 5-8). In this limit, diffusion-limited depletion at the surface is not explicitly modeled because turbulent mixing homogenizes the pool composition faster than surface evaporation depletes it. However, in keyhole-mode welding where local residence times are shorter, a concentration boundary layer can develop at the evaporating surface. In such cases, the surface concentration is depleted relative to the bulk, and the Mg flux is limited by liquid-phase diffusion of Mg to the surface. This is modeled using a diffusion boundary-layer approach, where the surface concentration falls below the bulk value.

### 4. Diffusion Coefficient of Mg in Liquid Al

Du et al. (2003, cited as Ref. [10] in Du et al. 2012, DOI: 10.1007/s11431-011-4692-6) systematically assessed impurity diffusion coefficients for several elements including Mg in both fcc and liquid Al using the CALPHAD/DICTRA framework. Their Figure 5 presents the temperature dependence of the impurity diffusion coefficient of Mg in fcc Al, validated against extensive experimental data (du2012atomicmobilitiesand pages 1-2, du2012atomicmobilitiesand pages 11-13). For liquid Al near and above the melting point (933 K), the self-diffusion coefficient of Al is of order 5–8 × 10⁻⁹ m²/s (Kargl et al. 2012, DOI: 10.1088/1742-6596/340/1/012077; Jakse and Pasturel 2013, DOI: 10.1038/srep03135), and Mg impurity diffusion in liquid Al is expected to be of similar magnitude. Zhao and DebRoy (2001) provide the gas-phase diffusivity of Mg in He shielding gas (Table V: D_{Mg-He} = [−1.10×10⁻² + 0.36T + 1.96×10⁻⁴T²]/P in mm²/s), which is used for the mass-transfer calculation at the gas side, not for liquid-metal diffusion (zhao2001weldmetalcomposition pages 5-8). The liquid-metal Mg diffusivity relevant for surface-depletion modeling should be taken from the Du et al. database or from molecular-dynamics calculations.

### 5. Measured Mg Loss

**Al 5182 laser welding:** Zhao and DebRoy (2001) report detailed measured and calculated Mg loss in conduction-mode Nd:YAG laser welding of AA5182 (Al–4.6Mg). The measured absolute Mg concentration decrease in the weld metal ranged from 0.47 to 0.66 wt% Mg (approximately 10–14% relative loss from the nominal ~4.6 wt% Mg), depending on laser power (1.5–3 kW) and welding speed (95–116 mm/s). Their Tables VIa and VIb provide calculated and experimental vaporization rates (0.32–0.76 mg/s) alongside the corresponding Mg depletion values (zhao2001weldmetalcomposition pages 8-9). Mg vapor flux was approximately two orders of magnitude greater than Al vapor flux (zhao2001weldmetalcomposition pages 5-8).

**LPBF AlSi10Mg:** AlSi10Mg contains only ~0.3 wt% Mg, so absolute Mg loss during LPBF is relatively small. Raza et al. (2021, DOI: 10.1016/j.matdes.2020.109358) studied AlSi10Mg powder degradation during LPBF and found changes in surface chemistry and oxide formation involving Mg. Deillon et al. (2022, DOI: 10.1016/j.jmatprotec.2021.117416) specifically addressed Mg evaporation prevention in LPBF of a high-Mg Al–Mg–Sc alloy (Calciscal®) through Ca addition. For high-Mg alloys processed by LPBF (e.g., Al–Mg–Sc with ~4–6 wt% Mg), significant Mg loss is expected and has been reported to reduce dissolved Mg content (sharma2022advancementsinthe pages 4-6).

### 6. Does Mg Vapour Lower the Keyhole Wall Temperature?

Yes. The effective boiling temperature of an Al–Mg alloy is substantially lower than that of pure Al because Mg's much higher vapor pressure means the total alloy vapor pressure reaches atmospheric pressure at a lower temperature. Zhao and DebRoy (2001) report the effective boiling point of AA5182 as approximately 1930 K, compared to ~2743 K for pure Al — a reduction of approximately 800 K (zhao2001weldmetalcomposition pages 5-8). Semenov et al. (2012) modeled the boiling temperature of Al–Mg alloys as a function of Mg mass fraction and found a sharp decrease as Mg content increases to ~2–3 wt%, with a weaker dependence at higher Mg concentrations (semenov2012modellingofbinary pages 3-6, semenov2012modellingofbinary pages 12-13). Additionally, the evaporative heat loss from preferential Mg vaporization acts as a significant cooling mechanism at the keyhole wall, with the evaporative heat flux potentially comparable to the arc/laser heat flux delivered to the surface (semenov2012modellingofbinary pages 9-12). For AlSi10Mg with ~0.3 wt% Mg, the boiling-point depression is much smaller than for 5xxx alloys, but the preferential evaporation of Mg still contributes to evaporative cooling.

The key thermodynamic and measured-composition inputs from the Zhao and DebRoy model are summarized in the following table:

| Quantity | Model input or value | Units and conditions | Source location |
|---|---:|---|---|
| Mg activity coefficient in dilute liquid Al | γ_Mg = 0.88; a_Mg = 0.88 x_Mg | Henry-law standard state; validate against CALPHAD for concentrated or Si-rich melts | Zhao and DebRoy (2001), DOI 10.1007/s11663-001-0018-6 (zhao2001weldmetalcomposition pages 2-3, moser1998newthermodynamicdata pages 4-5) |
| Pure-Mg equilibrium vapor pressure | log₁₀[P_Mg° (atm)] = 12.79 − 7550/T − 1.41 log₁₀T − log₁₀760 | T in K; alloy partial pressure p_Mg = a_Mg P_Mg° | Zhao and DebRoy (2001), Table V (zhao2001weldmetalcomposition pages 5-8) |
| Pure-Al equilibrium vapor pressure | log₁₀[P_Al° (atm)] = 12.36 − 16500/T − 1.02 log₁₀T − log₁₀760 | T in K; alloy partial pressure p_Al = a_Al P_Al° | Zhao and DebRoy (2001), Table V (zhao2001weldmetalcomposition pages 5-8) |
| Mg latent heat of vaporization | 5253 | J g⁻¹ | Zhao and DebRoy (2001), Table III (zhao2001weldmetalcomposition pages 4-5) |
| Al latent heat of vaporization | 10,780 | J g⁻¹ | Zhao and DebRoy (2001), Table III (zhao2001weldmetalcomposition pages 4-5) |
| Effective atmospheric-pressure boiling point of AA5182 | ≈1930 | K; total alloy vapor pressure equals ambient pressure | Zhao and DebRoy (2001), discussion of Fig. 7 (zhao2001weldmetalcomposition pages 5-8) |
| Pure-Al normal boiling point for comparison | ≈2743 | K; reference value, not the AA5182 value used in the model | Comparison with the sourced AA5182 result (zhao2001weldmetalcomposition pages 5-8) |
| Measured Mg concentration decrease in AA5182 weld metal | 0.47–0.66 | Absolute wt.% Mg decrease, not 47–66% relative loss; conduction-mode Nd:YAG welding | Zhao and DebRoy (2001), Tables VI(a) and VI(b) (zhao2001weldmetalcomposition pages 8-9) |
| Mg diffusivity in He shielding gas | D_Mg–He = [−1.10×10⁻² + 0.36T + 1.96×10⁻⁴T²]/P | mm² s⁻¹; T in K and P in atm; gas-phase diffusivity, not Mg diffusivity in liquid Al | Zhao and DebRoy (2001), Table V (zhao2001weldmetalcomposition pages 5-8) |


*Table: Key thermodynamic, vapor-pressure, latent-heat, gas-transport, and measured-composition inputs from Zhao and DebRoy’s AA5182 laser-welding model. The table distinguishes absolute wt.% Mg depletion and gas-phase diffusivity from liquid-metal diffusion.*

---

## Part (b): Powder-Layer Absorptance at 1.06–1.07 μm

### 1. Measured and Computed Absorptance Values

**Ray tracing (Boley et al. 2015):** Boley, Khairallah, and Rubenchik (2015, DOI: 10.1364/AO.54.002477) performed detailed ray-tracing calculations for metal powder beds at ~1 μm wavelength. For an ideal densely packed Al spherical array, they computed: flat-surface absorptivity 0.047, isolated-sphere absorptivity 0.056, top-layer absorption 0.15, total (spheres + substrate) absorptivity 0.22, giving a powder-to-flat-surface ratio of 4.7 (Table 1). For stainless steel, the total was 0.60 (ideal array), 0.58 (Gaussian size-distribution array), and 0.63 (bimodal array) (Table 2). Structure sensitivity is strongest for highly reflective metals like Al (king2015laserpowderbed pages 8-12, boley2015calculationoflaser pages 3-5, boley2015calculationoflaser pages 5-6).

**Calorimetry (Boley et al. 2016):** Boley et al. (2016, DOI: 10.1364/AO.55.006496) measured powder absorptivity using ~100 μm thick powder layers at ~1 μm and obtained A₀ = 0.53 for pure Al powder and A₀ = 0.58 for Al 6061 powder. These values significantly exceeded the ray-tracing prediction based on ideal optical constants (which predicts ~0.22), attributed to oxide layers and surface defects that increase the effective single-particle absorptivity to ~20% rather than the ideal 5% (boley2016metalpowderabsorptivity pages 5-5, boley2016metalpowderabsorptivity pages 1-2).

**In situ calorimetry (Trapp et al. 2017):** Trapp et al. (2017, DOI: 10.1016/j.apmt.2017.08.006) performed direct calorimetric absorptivity measurements at 1070 nm during LPBF scanning of Al 1100 and 316L SS. For powder layers at low power (pre-melting), the effective absorptivity was approximately twice that of polished bare substrates. Once the powder track was fully molten, absorptivity decreased; at higher power, keyhole formation caused absorptivity to rise again (trapp2017insituabsorptivity pages 1-2, trapp2017insituabsorptivity pages 4-6, trapp2017insituabsorptivity pages 8-9).

**Flat-surface measurement (Rubenchik et al. 2015):** Rubenchik et al. (2015, DOI: 10.1364/AO.54.007230) measured flat Al surface absorptivity at 970 nm as >20%, compared to the textbook Drude-Fresnel prediction of ~5%, demonstrating that the native oxide layer dominates real Al absorptivity (rubenchik2015directmeasurementsof pages 2-3).

**AlSi10Mg powder:** Solyaev et al. (2026, DOI: 10.1007/s00161-026-01516-x) estimated low-energy absorptivity values of approximately 0.20–0.30 for AlSi10Mg powder layers, depending on particle size fraction and packing density (solyaev2026ontheinfluence pages 23-26).

**Radiation transfer (Gusarov and Kruth 2005; Gusarov and Smurov 2009–2010):** The original Gusarov and Kruth (2005, DOI: 10.1016/j.ijheatmasstransfer.2005.01.044) model and its extensions establish a universal relationship for the absorptance of an optically thick (semi-infinite) powder bed as a function of the flat-surface absorptivity A_flat = 1 − ρ₁ (gusarov2010radiationtransferin pages 5-6, gusarov2010modelingtheinteraction pages 7-9):

**A_bed = 3·A_flat / (1 + 2·√A_flat)**

This formula (Eq. 21 in Gusarov and Smurov 2010, DOI: 10.1016/j.phpro.2010.08.065; Eq. 35 in Gusarov and Smurov 2010, DOI: 10.1016/j.jqsrt.2010.07.009) shows that bed absorptance is a universal function of single-particle absorptivity, independent of particle morphology and bed porosity in the optically thick limit. For A_flat = 0.05 (ideal Al), A_bed ≈ 0.11; for A_flat = 0.20 (oxidized Al), A_bed ≈ 0.33.

### 2. Dependence on Layer Thickness, Packing Density, and Particle Size

The absorptance of a finite powder layer increases with the layer's optical thickness τ = β·h, where h is the physical layer thickness and β is the extinction coefficient. For a layer on a substrate of the same material, absorptance increases monotonically from the substrate value toward the semi-infinite bed value as τ increases (gusarov2010radiationtransferin pages 10-11, gusarov2010radiationtransferin pages 6-8). Boley et al. (2015) showed that most energy is absorbed in the first one or two particle layers, with little more than 1% penetrating below two layers in idealized calculations (king2015laserpowderbed pages 8-12). Absorptivity fluctuations occur on a spatial scale of ~100 μm (much larger than particle diameter) and decrease with increasing beam size (boley2015calculationoflaser pages 3-5, boley2015calculationoflaser pages 5-6). Structure sensitivity is highest for highly reflective metals like Al and Au, where changes in powder geometry can alter absorptivity by nearly a factor of 2 (boley2015calculationoflaser pages 5-6).

### 3. Extinction Coefficient for Packed Beds of Opaque Spheres

For a statistically isotropic packed bed of large opaque spheres of diameter d with solid volume (packing) fraction φ and porosity f₀ = 1 − φ, the extinction coefficient in the geometrical-optics approximation is (gusarov2009amodelof pages 6-7, gusarov2010radiationtransferin pages 2-3, gusarov2010radiationtransferin pages 3-4, gusarov2009twodimensionalnumericalmodelling pages 1-2, gusarov2009amodelof pages 7-8, gusarov2010modelingtheinteraction pages 4-7):

**β = 3φ / [2d(1 − φ)]**

This is derived from the general relation β = A/(4f₀), where A = 6φ/d is the specific surface area of the spheres per unit total bed volume. The extinction coefficient increases with packing density and decreases inversely with particle diameter. For polydisperse powders, the specific surface A is computed from the particle size distribution.

### 4. Typical AlSi10Mg Powder-Layer Packing Densities

Solyaev et al. (2026, DOI: 10.1007/s00161-026-01516-x, Table 1) report spread-layer packing fractions for gas-atomized AlSi10Mg powder of φ = 0.380–0.433 for different sieved fractions, while volumetric (tapped/settled) packing fractions were higher at approximately 0.528–0.542 (solyaev2026ontheinfluence pages 3-6). These are consistent with typical LPBF powder-layer packing densities of ~40–60% of theoretical for gas-atomized spherical powders.

The following table summarizes all powder absorptance data, the extinction coefficient formula, and packing density values:

| Material / model | Method and wavelength | Absorptance result | Thickness, packing, or particle-size relevance | Source |
|---|---|---:|---|---|
| Pure Al | Fresnel ray tracing near 1 µm | Flat surface: **0.047**; isolated sphere: **0.056**; top particle layer: **0.150**; bottom layer: **0.063**; substrate: **0.011**; total spheres + substrate: **0.220**; powder/flat ratio: **4.7** | Ideal, densely packed spherical array; most absorption occurs in the first two particle layers | Boley, Khairallah & Rubenchik (2015), **Table 1**, DOI: [10.1364/AO.54.002477](https://doi.org/10.1364/AO.54.002477) (boley2015calculationoflaser pages 3-5) |
| Pure Al powder | Experiment/model comparison near 1 µm | Fitted/measured powder value **A₀ = 0.53** | Approximately **100 µm** powder thickness; measured absorption exceeded ideal optical-data predictions because oxide, roughness, and particle defects raised the effective particle absorptance | Boley et al. (2016), DOI: [10.1364/AO.55.006496](https://doi.org/10.1364/AO.55.006496) (boley2016metalpowderabsorptivity pages 5-5) |
| Al 6061 powder | Experiment/model comparison near 1 µm | Fitted/measured powder value **A₀ = 0.58** | Approximately **100 µm** powder thickness; result is an effective powder-bed value rather than intrinsic smooth-surface absorptance | Boley et al. (2016), DOI: [10.1364/AO.55.006496](https://doi.org/10.1364/AO.55.006496) (boley2016metalpowderabsorptivity pages 5-5) |
| Al 1100 powder on Al substrate | Direct scanning calorimetry at **1070 nm** | Before complete melting, powder-layer absorptance was approximately **2×** that of the polished plate; no reliable absolute Al value is printed in the accessible text | About **100 µm** powder; absorptance falls when the layer becomes a continuous molten track and rises again at keyhole onset | Trapp et al. (2017), **Figs. 3–6 / regime discussion**, DOI: [10.1016/j.apmt.2017.08.006](https://doi.org/10.1016/j.apmt.2017.08.006) (trapp2017insituabsorptivity pages 1-2, trapp2017insituabsorptivity pages 4-6, trapp2017insituabsorptivity pages 8-9) |
| Flat Al and pure-Al powder | Direct calorimetry at **970 nm**, used as a proxy for ∼1 µm LPBF lasers | Flat Al measured **>0.20**, versus approximately **0.05** from ideal handbook optical constants; oxide and surface structure dominate the discrepancy | Demonstrates why Drude/Fresnel values for clean Al can seriously underpredict real powder absorptance | Rubenchik et al. (2015), DOI: [10.1364/AO.54.007230](https://doi.org/10.1364/AO.54.007230) (rubenchik2015directmeasurementsof pages 2-3) |
| AlSi10Mg powder | Low-energy absorptance inferred for particle-size-resolved powder layers | Approximately **0.20–0.30** | Optical thickness is \(\tau=\beta h\); smaller particles and denser/thicker layers generally increase \(\tau\), although surface oxide and powder morphology can alter the intrinsic particle reflectivity | Solyaev et al. (2026), discussion around **Fig. 2 and Eq. 12**, DOI: [10.1007/s00161-026-01516-x](https://doi.org/10.1007/s00161-026-01516-x) (solyaev2026ontheinfluence pages 26-28, solyaev2026ontheinfluence pages 23-26) |
| Optically thick opaque-particle bed | Homogenized radiation-transfer model | \(A_{bed}=\dfrac{3A_{flat}}{1+2\sqrt{A_{flat}}}\), with \(A_{flat}=1-\rho_1\) under the model’s reflectivity convention | Semi-infinite limit: bed absorptance approaches a material-controlled value; morphology, density, and particle diameter chiefly determine how rapidly a finite layer reaches that limit | Gusarov & Smurov (2010), **Eq. 21**, DOI: [10.1016/j.phpro.2010.08.065](https://doi.org/10.1016/j.phpro.2010.08.065); related thick-bed relation and **Fig. 2** in DOI: [10.1016/j.jqsrt.2010.07.009](https://doi.org/10.1016/j.jqsrt.2010.07.009) (gusarov2010modelingtheinteraction pages 7-9, gusarov2010radiationtransferin pages 6-8) |
| Monodisperse packed bed of opaque spheres | Geometrical-optics radiation transfer | Extinction coefficient: \(\beta=\dfrac{3\phi}{2d(1-\phi)}\), where \(\phi\) is solid packing fraction and \(d\) is particle diameter | Hence \(\beta\propto 1/d\), increases with \(\phi\), and finite-layer optical thickness is \(\tau=\beta h\) | Gusarov & Smurov (2009–2010), DOI: [10.1016/j.apsusc.2008.07.202](https://doi.org/10.1016/j.apsusc.2008.07.202) and [10.1016/j.phpro.2010.08.065](https://doi.org/10.1016/j.phpro.2010.08.065) (gusarov2009twodimensionalnumericalmodelling pages 1-2, gusarov2010modelingtheinteraction pages 4-7) |
| Gas-atomized AlSi10Mg powder layers | Apparent-density measurements, \(\phi=\rho_a/\rho_s\) | Representative spread-layer packing fractions: **0.380–0.433** | Reported values include **0.432, 0.380, 0.421, and 0.433** for standard and sieved fractions; corresponding bulk-volume samples were denser, approximately **0.528–0.542** | Solyaev et al. (2026), **Table 1**, DOI: [10.1007/s00161-026-01516-x](https://doi.org/10.1007/s00161-026-01516-x) (solyaev2026ontheinfluence pages 3-6) |


*Table: Measured and modeled near-infrared absorptance for Al, Al alloys, and AlSi10Mg powder beds, together with the packed-sphere extinction relation and representative AlSi10Mg packing fractions. Values from different methods are not interchangeable because oxidation, layer state, and optical thickness strongly affect effective absorptance.*

### Key DOIs and Figure/Table References

- Zhao and DebRoy (2001): DOI 10.1007/s11663-001-0018-6 — Tables III, IV, V, VIa, VIb; Figs. 7–10
- Semenov et al. (2012): DOI 10.1088/0965-0393/20/5/055009 — Figs. 5–8
- Moser et al. (1998): DOI 10.1361/105497198770342733 — vapor-pressure and activity data tables
- He et al. (2003): DOI 10.1088/0022-3727/36/23/033
- Du et al. (2012): DOI 10.1007/s11431-011-4692-6 — Fig. 5 (Mg impurity diffusion in Al)
- Boley et al. (2015): DOI 10.1364/AO.54.002477 — Tables 1, 2; Figs. 3–10
- Boley et al. (2016): DOI 10.1364/AO.55.006496 — absorptivity measurements
- Rubenchik et al. (2015): DOI 10.1364/AO.54.007230 — temperature-dependent powder absorptivity
- Trapp et al. (2017): DOI 10.1016/j.apmt.2017.08.006 — Figs. 3–6
- Gusarov and Smurov (2010): DOI 10.1016/j.jqsrt.2010.07.009 — Eq. 35, Fig. 2; DOI 10.1016/j.phpro.2010.08.065 — Eq. 21
- Gusarov and Smurov (2009): DOI 10.1016/j.apsusc.2008.07.202 — extinction coefficient derivation
- Gusarov and Kruth (2005): DOI 10.1016/j.ijheatmasstransfer.2005.01.044 — original universal absorptance function
- Solyaev et al. (2026): DOI 10.1007/s00161-026-01516-x — Table 1 (packing densities), Fig. 2 (extinction coefficients)
- Raza et al. (2021): DOI 10.1016/j.matdes.2020.109358 — AlSi10Mg powder degradation
- Deillon et al. (2022): DOI 10.1016/j.jmatprotec.2021.117416 — Ca addition to prevent Mg evaporation in LPBF

References

1. (zhao2001weldmetalcomposition pages 2-3): H. Zhao and T. Debroy. Weld metal composition change during conduction mode laser welding of aluminum alloy 5182. Metallurgical and Materials Transactions B, 32:163-172, Feb 2001. URL: https://doi.org/10.1007/s11663-001-0018-6, doi:10.1007/s11663-001-0018-6. This article has 274 citations.

2. (semenov2012modellingofbinary pages 3-6): I. Semenov, I. Krivtsun, V. Demchenko, A. Semenov, U. Reisgen, O. Mokrov, and A. Zabirov. Modelling of binary alloy (al–mg) anode evaporation in arc welding. Modelling and Simulation in Materials Science and Engineering, 20:055009, Jul 2012. URL: https://doi.org/10.1088/0965-0393/20/5/055009, doi:10.1088/0965-0393/20/5/055009. This article has 16 citations and is from a peer-reviewed journal.

3. (moser1998newthermodynamicdata pages 4-5): Z. Moser, W. Zakulski, K. Rzyman, W. Gasior, Z. Panek, I. Katayama, T. Matsuda, Y. Fukuda, T. Iida, Z. Zajaczkowski, and J. Botor. New thermodynamic data for liquid aluminum-magnesium alloys from emf, vapor pressures, and calorimetric studies. Feb 1998. URL: https://doi.org/10.1361/105497198770342733, doi:10.1361/105497198770342733. This article has 36 citations.

4. (moser1998newthermodynamicdata pages 3-4): Z. Moser, W. Zakulski, K. Rzyman, W. Gasior, Z. Panek, I. Katayama, T. Matsuda, Y. Fukuda, T. Iida, Z. Zajaczkowski, and J. Botor. New thermodynamic data for liquid aluminum-magnesium alloys from emf, vapor pressures, and calorimetric studies. Feb 1998. URL: https://doi.org/10.1361/105497198770342733, doi:10.1361/105497198770342733. This article has 36 citations.

5. (zhao2001weldmetalcomposition pages 3-4): H. Zhao and T. Debroy. Weld metal composition change during conduction mode laser welding of aluminum alloy 5182. Metallurgical and Materials Transactions B, 32:163-172, Feb 2001. URL: https://doi.org/10.1007/s11663-001-0018-6, doi:10.1007/s11663-001-0018-6. This article has 274 citations.

6. (zhao2001weldmetalcomposition pages 4-5): H. Zhao and T. Debroy. Weld metal composition change during conduction mode laser welding of aluminum alloy 5182. Metallurgical and Materials Transactions B, 32:163-172, Feb 2001. URL: https://doi.org/10.1007/s11663-001-0018-6, doi:10.1007/s11663-001-0018-6. This article has 274 citations.

7. (semenov2012modellingofbinary pages 6-9): I. Semenov, I. Krivtsun, V. Demchenko, A. Semenov, U. Reisgen, O. Mokrov, and A. Zabirov. Modelling of binary alloy (al–mg) anode evaporation in arc welding. Modelling and Simulation in Materials Science and Engineering, 20:055009, Jul 2012. URL: https://doi.org/10.1088/0965-0393/20/5/055009, doi:10.1088/0965-0393/20/5/055009. This article has 16 citations and is from a peer-reviewed journal.

8. (liu2017compositionchangeof pages 3-5): T Liu, LJ Yang, HL Wei, WC Qiu, and T Debroy. Composition change of stainless steels during keyhole mode laser welding. Unknown journal, 2017.

9. (he2003alloyingelementvaporization pages 2-3): X. He, T. DebRoy, and P. W. Fuerschbach. Alloying element vaporization during laser spot welding of stainless steel. Nov 2003. URL: https://doi.org/10.1088/0022-3727/36/23/033, doi:10.1088/0022-3727/36/23/033. This article has 142 citations and is from a peer-reviewed journal.

10. (zhao2001weldmetalcomposition pages 5-8): H. Zhao and T. Debroy. Weld metal composition change during conduction mode laser welding of aluminum alloy 5182. Metallurgical and Materials Transactions B, 32:163-172, Feb 2001. URL: https://doi.org/10.1007/s11663-001-0018-6, doi:10.1007/s11663-001-0018-6. This article has 274 citations.

11. (du2012atomicmobilitiesand pages 1-2): Yong Du, LiJun Zhang, SenLin Cui, DongDong Zhao, DanDan Liu, WeiBin Zhang, WeiHua Sun, and WanQi Jie. Atomic mobilities and diffusivities in al alloys. Science China Technological Sciences, 55:306-328, Dec 2012. URL: https://doi.org/10.1007/s11431-011-4692-6, doi:10.1007/s11431-011-4692-6. This article has 46 citations.

12. (du2012atomicmobilitiesand pages 11-13): Yong Du, LiJun Zhang, SenLin Cui, DongDong Zhao, DanDan Liu, WeiBin Zhang, WeiHua Sun, and WanQi Jie. Atomic mobilities and diffusivities in al alloys. Science China Technological Sciences, 55:306-328, Dec 2012. URL: https://doi.org/10.1007/s11431-011-4692-6, doi:10.1007/s11431-011-4692-6. This article has 46 citations.

13. (zhao2001weldmetalcomposition pages 8-9): H. Zhao and T. Debroy. Weld metal composition change during conduction mode laser welding of aluminum alloy 5182. Metallurgical and Materials Transactions B, 32:163-172, Feb 2001. URL: https://doi.org/10.1007/s11663-001-0018-6, doi:10.1007/s11663-001-0018-6. This article has 274 citations.

14. (sharma2022advancementsinthe pages 4-6): Sachin Kumar Sharma, Harpreet Singh Grewal, Kuldeep Kumar Saxena, Kahtan A. Mohammed, Chander Prakash, J. Paulo Davim, Dharam Buddhi, Ramesh Raju, Dhanesh G. Mohan, and Jacek Tomków. Advancements in the additive manufacturing of magnesium and aluminum alloys through laser-based approach. Materials, 15:8122, Nov 2022. URL: https://doi.org/10.3390/ma15228122, doi:10.3390/ma15228122. This article has 51 citations.

15. (semenov2012modellingofbinary pages 12-13): I. Semenov, I. Krivtsun, V. Demchenko, A. Semenov, U. Reisgen, O. Mokrov, and A. Zabirov. Modelling of binary alloy (al–mg) anode evaporation in arc welding. Modelling and Simulation in Materials Science and Engineering, 20:055009, Jul 2012. URL: https://doi.org/10.1088/0965-0393/20/5/055009, doi:10.1088/0965-0393/20/5/055009. This article has 16 citations and is from a peer-reviewed journal.

16. (semenov2012modellingofbinary pages 9-12): I. Semenov, I. Krivtsun, V. Demchenko, A. Semenov, U. Reisgen, O. Mokrov, and A. Zabirov. Modelling of binary alloy (al–mg) anode evaporation in arc welding. Modelling and Simulation in Materials Science and Engineering, 20:055009, Jul 2012. URL: https://doi.org/10.1088/0965-0393/20/5/055009, doi:10.1088/0965-0393/20/5/055009. This article has 16 citations and is from a peer-reviewed journal.

17. (king2015laserpowderbed pages 8-12): W. E. King, A. T. Anderson, R. M. Ferencz, N. E. Hodge, C. Kamath, S. A. Khairallah, and A. M. Rubenchik. Laser powder bed fusion additive manufacturing of metals; physics, computational, and materials challenges. Applied physics reviews, 2:041304, Dec 2015. URL: https://doi.org/10.1063/1.4937809, doi:10.1063/1.4937809. This article has 1901 citations and is from a domain leading peer-reviewed journal.

18. (boley2015calculationoflaser pages 3-5): C. D. Boley, S. A. Khairallah, and A. M. Rubenchik. Calculation of laser absorption by metal powders in additive manufacturing. Applied optics, 54 9:2477-82, Mar 2015. URL: https://doi.org/10.1364/ao.54.002477, doi:10.1364/ao.54.002477. This article has 538 citations and is from a peer-reviewed journal.

19. (boley2015calculationoflaser pages 5-6): C. D. Boley, S. A. Khairallah, and A. M. Rubenchik. Calculation of laser absorption by metal powders in additive manufacturing. Applied optics, 54 9:2477-82, Mar 2015. URL: https://doi.org/10.1364/ao.54.002477, doi:10.1364/ao.54.002477. This article has 538 citations and is from a peer-reviewed journal.

20. (boley2016metalpowderabsorptivity pages 5-5): C. D. Boley, S. C. Mitchell, A. M. Rubenchik, and S. S. Q. Wu. Metal powder absorptivity: modeling and experiment. Applied optics, 55 23:6496-500, Aug 2016. URL: https://doi.org/10.1364/ao.55.006496, doi:10.1364/ao.55.006496. This article has 235 citations and is from a peer-reviewed journal.

21. (boley2016metalpowderabsorptivity pages 1-2): C. D. Boley, S. C. Mitchell, A. M. Rubenchik, and S. S. Q. Wu. Metal powder absorptivity: modeling and experiment. Applied optics, 55 23:6496-500, Aug 2016. URL: https://doi.org/10.1364/ao.55.006496, doi:10.1364/ao.55.006496. This article has 235 citations and is from a peer-reviewed journal.

22. (trapp2017insituabsorptivity pages 1-2): Johannes Trapp, Alexander M. Rubenchik, Gabe Guss, and Manyalibo J. Matthews. In situ absorptivity measurements of metallic powders during laser powder-bed fusion additive manufacturing. Applied Materials Today, 9:341-349, Dec 2017. URL: https://doi.org/10.1016/j.apmt.2017.08.006, doi:10.1016/j.apmt.2017.08.006. This article has 666 citations and is from a peer-reviewed journal.

23. (trapp2017insituabsorptivity pages 4-6): Johannes Trapp, Alexander M. Rubenchik, Gabe Guss, and Manyalibo J. Matthews. In situ absorptivity measurements of metallic powders during laser powder-bed fusion additive manufacturing. Applied Materials Today, 9:341-349, Dec 2017. URL: https://doi.org/10.1016/j.apmt.2017.08.006, doi:10.1016/j.apmt.2017.08.006. This article has 666 citations and is from a peer-reviewed journal.

24. (trapp2017insituabsorptivity pages 8-9): Johannes Trapp, Alexander M. Rubenchik, Gabe Guss, and Manyalibo J. Matthews. In situ absorptivity measurements of metallic powders during laser powder-bed fusion additive manufacturing. Applied Materials Today, 9:341-349, Dec 2017. URL: https://doi.org/10.1016/j.apmt.2017.08.006, doi:10.1016/j.apmt.2017.08.006. This article has 666 citations and is from a peer-reviewed journal.

25. (rubenchik2015directmeasurementsof pages 2-3): A. Rubenchik, Sheldon Wu, Scott C. Mitchell, I. Golosker, M. Leblanc, and N. Peterson. Direct measurements of temperature-dependent laser absorptivity of metal powders. Applied optics, 54 24:7230-3, Aug 2015. URL: https://doi.org/10.1364/ao.54.007230, doi:10.1364/ao.54.007230. This article has 134 citations and is from a peer-reviewed journal.

26. (solyaev2026ontheinfluence pages 23-26): Y. Solyaev, V. Dobryanskiy, Nguyen Long, and Stanislav Chernyshikhin. On the influence of powder particle size on single-track formation in laser powder bed fusion of alsi10mg alloy. Continuum Mechanics and Thermodynamics, Jul 2026. URL: https://doi.org/10.1007/s00161-026-01516-x, doi:10.1007/s00161-026-01516-x. This article has 1 citations and is from a peer-reviewed journal.

27. (gusarov2010radiationtransferin pages 5-6): A.V. Gusarov and I. Smurov. Radiation transfer in metallic powder beds used in laser processing. Journal of Quantitative Spectroscopy & Radiative Transfer, 111:2517-2527, Nov 2010. URL: https://doi.org/10.1016/j.jqsrt.2010.07.009, doi:10.1016/j.jqsrt.2010.07.009. This article has 54 citations and is from a peer-reviewed journal.

28. (gusarov2010modelingtheinteraction pages 7-9): A.V. Gusarov and I. Smurov. Modeling the interaction of laser radiation with powder bed at selective laser melting. Physics Procedia, 5:381-394, Jan 2010. URL: https://doi.org/10.1016/j.phpro.2010.08.065, doi:10.1016/j.phpro.2010.08.065. This article has 333 citations and is from a peer-reviewed journal.

29. (gusarov2010radiationtransferin pages 10-11): A.V. Gusarov and I. Smurov. Radiation transfer in metallic powder beds used in laser processing. Journal of Quantitative Spectroscopy & Radiative Transfer, 111:2517-2527, Nov 2010. URL: https://doi.org/10.1016/j.jqsrt.2010.07.009, doi:10.1016/j.jqsrt.2010.07.009. This article has 54 citations and is from a peer-reviewed journal.

30. (gusarov2010radiationtransferin pages 6-8): A.V. Gusarov and I. Smurov. Radiation transfer in metallic powder beds used in laser processing. Journal of Quantitative Spectroscopy & Radiative Transfer, 111:2517-2527, Nov 2010. URL: https://doi.org/10.1016/j.jqsrt.2010.07.009, doi:10.1016/j.jqsrt.2010.07.009. This article has 54 citations and is from a peer-reviewed journal.

31. (gusarov2009amodelof pages 6-7): A. V. Gusarov. A model of averaged radiation transfer in two-phase heterogeneous medium. High Temperature, 47:375-389, Jun 2009. URL: https://doi.org/10.1134/s0018151x09030110, doi:10.1134/s0018151x09030110. This article has 14 citations and is from a peer-reviewed journal.

32. (gusarov2010radiationtransferin pages 2-3): A.V. Gusarov and I. Smurov. Radiation transfer in metallic powder beds used in laser processing. Journal of Quantitative Spectroscopy & Radiative Transfer, 111:2517-2527, Nov 2010. URL: https://doi.org/10.1016/j.jqsrt.2010.07.009, doi:10.1016/j.jqsrt.2010.07.009. This article has 54 citations and is from a peer-reviewed journal.

33. (gusarov2010radiationtransferin pages 3-4): A.V. Gusarov and I. Smurov. Radiation transfer in metallic powder beds used in laser processing. Journal of Quantitative Spectroscopy & Radiative Transfer, 111:2517-2527, Nov 2010. URL: https://doi.org/10.1016/j.jqsrt.2010.07.009, doi:10.1016/j.jqsrt.2010.07.009. This article has 54 citations and is from a peer-reviewed journal.

34. (gusarov2009twodimensionalnumericalmodelling pages 1-2): A.V. Gusarov and I. Smurov. Two-dimensional numerical modelling of radiation transfer in powder beds at selective laser melting. Applied Surface Science, 255:5595-5599, Mar 2009. URL: https://doi.org/10.1016/j.apsusc.2008.07.202, doi:10.1016/j.apsusc.2008.07.202. This article has 65 citations and is from a domain leading peer-reviewed journal.

35. (gusarov2009amodelof pages 7-8): A. V. Gusarov. A model of averaged radiation transfer in two-phase heterogeneous medium. High Temperature, 47:375-389, Jun 2009. URL: https://doi.org/10.1134/s0018151x09030110, doi:10.1134/s0018151x09030110. This article has 14 citations and is from a peer-reviewed journal.

36. (gusarov2010modelingtheinteraction pages 4-7): A.V. Gusarov and I. Smurov. Modeling the interaction of laser radiation with powder bed at selective laser melting. Physics Procedia, 5:381-394, Jan 2010. URL: https://doi.org/10.1016/j.phpro.2010.08.065, doi:10.1016/j.phpro.2010.08.065. This article has 333 citations and is from a peer-reviewed journal.

37. (solyaev2026ontheinfluence pages 3-6): Y. Solyaev, V. Dobryanskiy, Nguyen Long, and Stanislav Chernyshikhin. On the influence of powder particle size on single-track formation in laser powder bed fusion of alsi10mg alloy. Continuum Mechanics and Thermodynamics, Jul 2026. URL: https://doi.org/10.1007/s00161-026-01516-x, doi:10.1007/s00161-026-01516-x. This article has 1 citations and is from a peer-reviewed journal.

38. (solyaev2026ontheinfluence pages 26-28): Y. Solyaev, V. Dobryanskiy, Nguyen Long, and Stanislav Chernyshikhin. On the influence of powder particle size on single-track formation in laser powder bed fusion of alsi10mg alloy. Continuum Mechanics and Thermodynamics, Jul 2026. URL: https://doi.org/10.1007/s00161-026-01516-x, doi:10.1007/s00161-026-01516-x. This article has 1 citations and is from a peer-reviewed journal.
