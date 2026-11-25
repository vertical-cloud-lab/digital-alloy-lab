# Review of the physics-based truth

## Bottom line

**I would not use this model to justify excluding alloys below 10–15 wt% Ni.** It is a useful physics-informed synthetic benchmark, but the nickel floor is neither a measured threshold nor robust to reasonable modeling choices.

I found two important problems before changing any corrosion assumptions:

1. **The reported floors are minima in 400,000 random designs, not optimized floors.** With the supplied constants and feasibility rules, I found passing designs at **12.51 wt% Ni against C71500** and **6.41 wt% Ni against C70600**. Numerical minimization gives approximately **12.50 and 6.40 wt%**, respectively—not 14.6 and 9.2.
2. **The reference is not dense wrought material.** The code uses a simulated deposited reference with relative density 0.908 for C71500 and 0.978 for C70600. Making those reference coupons genuinely dense, while otherwise retaining the model, changes the optimized floors to approximately **15.97 and 6.97 wt% Ni**.

The fit reproduces its saved output, but its conclusions depend strongly on transferring measurements between durations and environments, assigning an unidentified aluminum bronze the composition of C61400, downweighting short-time composition-series data, choosing the Ni dependence, and choosing the retained matrix composition.

### What I ran

I reproduced the corrosion fit: weighted log-residual sum of squares **0.59508**, with the saved parameters. I also reproduced both 400,000-design landscape checks and their reported optima using an import adapter. The original scripts fail as uploaded because `physics` and `bofn_alloy` are absent. My adapter uses `truth_phys.feasible`; it explicitly omits the unavailable shared-seed-design statistic rather than inventing it.

I independently checked the interpolation against SciPy and validated a faster NumPy evaluator against the supplied PyTorch truth. Numerical differences were at floating-point precision.

**Files:** [parameters and floors](review/refit_parameters_and_floors.csv), [optimized witnesses](review/floor_sensitivities_verified.json), [bar/density checks](review/floor_bar_and_density_checks.json), [executable audit](review/audit_reproduce.py), and [reproduction instructions](review/REPRODUCE.txt). I left the uploaded files unchanged.

## 1. Corrosion model and calibration

### What the cited evidence supports—and does not support

I checked the retrieved primary texts of [Lewis and LaQue, 1981](https://doi.org/10.2172/6255887), [Yongchao Yang’s 2019 thesis](https://doi.org/10.26190/unsworks/21760), and [Ran Yang et al., 2018](https://doi.org/10.3390/ma11091777). I used no publication by Sterling G. Baird.

These sources support time-dependent protection, a substantial Fe effect in a particular Cu–10Ni test, and composition-dependent corrosion. **They do not identify this particular seven-parameter, cross-family, 30-day model.**

| Calibration choice | Assessment |
|---|---|
| C70600/C71500 target **1.4 at 30 days** | A discretionary compromise, not an observed same-test 30-day ratio. The actual 30-day clean-seawater duplicates give **0.9686** from the ratio of means. The other cited ratios concern 62 days and one year under different flow conditions. |
| Cu/C71500 target **3 at 30 days** | A constructed target, not a matched 30-day observation in the supplied evidence. |
| Aluminum bronze/C71500 target **2.1 at 30 days**, assigning C61400 chemistry | The source comparison is **one year**, and the bronze grade, chemistry and phase condition are unreported. Assigning Cu–7Al–2.5Fe and moving it to 30 days are consequential assumptions. |
| Fe protection | The reported 60-day rates, 38.4 versus 12.2 µm/year, support a strong effect at fixed nominal 10% Ni. They do not establish the **1.5 wt% solution-Fe cap**, transferability to Al-containing alloys, or a universal coefficient. |
| Late/early Ni protection | The 0.70/0.36/0.18 ratios appear in Lewis and LaQue. The fit additionally assigns **0.5 wt% Fe** to the Cu–20Ni and Cu–30Ni specimens, which is not specified in that reproduced table. |
| Linear Ni feature | A modeling choice. The evidence does not establish linearity of log transport with **retained alpha-matrix Ni** through 30 wt%, especially across Cu–Ni–Al alloys. |
| Residual weights | Arbitrary rather than measurement-error-based. Multiplying a residual by 0.5 gives it **one-quarter** the squared-error weight of a weight-1 residual. This suppresses the short-time evidence for Al protection. |

The fitted model misses important observations substantially: Cu–28.4Ni at two hours is **5.05 versus 2.48 µA/cm²**, Cu–7Al is **5.51 versus 3.16**, and the first-month C71500 current is **1.12 versus the chosen target 2.0**. These are not small residuals around a validated constitutive law.

### The model structure is plausible as a surrogate, not established physics

- **Film kinetics:** A parabolic transient plus a steady term can represent decaying and persistent corrosion. But inserting a time-varying `K_cu*q(t)` directly into `sqrt(K/(2t))` is not a film-thickness evolution calculation: the film has no integrated growth/dissolution history. The model is best described as a phenomenological current-decay law.
- **“Mixed potential”:** There is no potential or anodic/cathodic polarization balance. The harmonic-current expression is a resistance/limitation analogy, not a solved mixed-potential model.
- **Oxygen limit:** The steady term is added **outside** the oxygen-limited branch; selective attack is also added separately. Consequently, 30 µA/cm² is not a limit on the total modeled corrosion current. For fresh pure Cu, the limiting expression as time approaches zero is **33.604**, not 30 µA/cm². If all sustained attack is oxygen-supported, the cathodic budget needs to constrain the total.
- **Fast Al versus slow Ni/Fe:** Qualitatively plausible, but one maturation time and these element-specific allocations are not measured by the calibration data. The implemented fitted time is **10 days**, not the three days described in the module introduction.
- **Selective beta-prime attack:** The rate, one-day incubation, and proportionality to retained beta fraction are unmeasured priors. They are not calibrated by the fitted observations, which are modeled as dense and beta-free.
- **Porosity:** `1 + (1-rho)` is an assumed multiplier bounded by two. Bulk density alone does not determine exposed internal area, pore connectivity or crevice chemistry.

### Optimized floors under alternative fits

The following table uses the code’s **deposited-reference convention**. I recomputed both reference bars under every fit, compared raw integrated mass loss, and minimized Ni over the remaining composition and process variables within the supplied feasibility rules. These are numerical optima, not formal proofs of global optimality or confidence intervals.

| Fit or assumption | Minimum Ni: C71500 bar | Minimum Ni: C70600 bar |
|---|---:|---:|
| Original targets, weights and bounds, refitted | **12.51** | **6.40** |
| Replace 1.4 with actual 30-day duplicate-mean ratio **0.9686** | **7.61** | **5.98** |
| Replace 1.4 with **2.3**, representing the 62-day comparison | 16.73 | 5.31 |
| Omit constructed Cu ratio and unidentified one-year bronze target | **0.00** | **0.00** |
| Equal weights on log residuals | 13.47 | 4.40 |
| Full weight on two-hour data; omit Cu and one-year bronze ratio targets | 1.38 | 0.00 |
| Allow `a_al` below 0.05 | 12.38 | 6.82 |
| Allow maturation time up to 100 days | 15.35 | 6.53 |
| Allow `K_cu` below 100,000, down to 1 | 12.69 | 6.43 |
| Relax all three active bounds, with broader coefficient bounds | 15.38 | 6.49 |
| Fix `a_al = 0.4`; refit other constants | 4.98 | 0.00 |
| Fix maturation time at three days; refit | 11.36 | 6.44 |
| Fix `K_cu = 10⁷`; refit | 16.03 | 4.59 |
| Add Yang 2018, using its **source-matched control chemistry** | 12.50 | 4.50 |
| Saturating Ni feature, characteristic scale 10 wt% | **5.56** | **6.96** |
| Nominal composition instead of 900 °C matrix; refit | 12.86 | 4.08 |
| Raise solution-Fe protection cap from 1.5 to 3 wt% | 10.33 | 6.15 |

The zero-Ni alternatives are **not predictions I endorse for real alloys**. They demonstrate that excluding weakly transferable targets can change the fitted Al contribution enough to remove the model’s floor. One zero-Ni witness against C71500 is approximately Cu–5.29Al–1.67Fe, with modeled density **0.980**; this particular result is not merely a zero-density optimization artifact.

The saturating feature was normalized to equal one at 30 wt% Ni. Its fit loss is **0.749**, versus **0.595** originally. Under that alternative, the two reference bars need not preserve their original ordering because their Fe contents differ—another reason not to interpret the fitted landscape as an established Ni-only law.

### Which bound-hitting constants matter?

**For the C71500 floor, the maturation-time bound matters most when simply releasing the active bounds.**

- Releasing the **Al lower bound** yields `a_al ≈ 0.030`, with little change: **12.51 → 12.38 wt% Ni**. Thus, the imposed minimum 0.05 is not itself what makes Al weak. The targets and weights favor a weak Al contribution. Removing questionable targets instead gives `a_al ≈ 0.45` and eliminates the floor.
- Releasing the **K lower bound** changes the fit substantially but barely moves these floors: **12.51 → 12.69**, **6.40 → 6.43**. The steady term compensates for the transient term. A much larger imposed K does move the floors, but worsens the original fit loss to **2.165**.
- Releasing the **10-day upper bound** moves the fitted time to approximately **56.7 days**, with Fe protection reaching its own upper bound, and moves the C71500 floor to **15.35**. The C70600 floor remains near **6.53**. This is parameter trade-off, not a measurement of a 57-day film time.

Boundary solutions can indicate insufficient information, conflicting data, or structural misspecification—not just parameters that “cannot be separated.” Here all three possibilities matter.

### The 900 °C matrix assumption is consequential

A 900 °C equilibrium alpha composition is neither the Scheil segregated matrix nor a kinetic prediction of the DED room-temperature microstructure. Choosing it because 700 °C gives unrealistic NAB partitioning is understandable, but it is an empirical workaround for database/kinetic limitations.

Using the 700 °C matrix and refitting gives floors of **16.82/7.63 wt%** if I require candidate density at least 0.95. Without that additional requirement, the literal code permits approximately **1.30/0.95 wt%**, by exploiting almost zero density and process settings that suppress modeled beta retention. This illustrates a feasibility problem, not evidence for those alloys.

Two other unmeasured assumptions matter: setting selective attack to zero moves the C70600-bar floor from **6.40 to 2.99 wt%**; removing the porosity multiplier moves the floors to **15.61/6.84**, partly because it also tightens the C71500 reference.

## 2. CALPHAD grid, physical mappings and bugs

### The interpolation implementation is correct

I found **864 unique compositions**, no missing liquidus/solidus or 99%-solid temperatures, and no liquidus below solidus. The **810 converged / 54 non-converged** Scheil count is correct; all rows contain a 99%-solid temperature.

For 1,000 random compositions, all 16 interpolated fields agreed with SciPy’s multilinear interpolator to numerical precision; the maximum absolute discrepancy was approximately **7 × 10⁻¹³**.

That validates the interpolation arithmetic, **not** the thermodynamic database or phase identifications. Independent interpolation of phase fractions and conditional matrix compositions can smear phase boundaries and need not preserve a thermodynamically consistent phase assemblage or component balance.

### The phase-to-property mappings are much less secure

| Mapping | Finding |
|---|---|
| Scheil range → crack index | A possible screening descriptor, not a validated cracking prediction. Hot tearing depends on late-stage feeding, coherency, strain and cooling conditions, not total range alone. `/250`, the 200 K onset and nucleant correction are assumed. Clamping the index at one also discards differences above 250 K. The onset was deliberately adjusted to make the reference deposit relatively dense. |
| Beta at 900 °C → retained beta-prime | High-temperature beta fraction is a tendency, not retained martensite fraction. Transformation temperatures, kinetics, segregation and repeated thermal cycles are absent. The logistic process factor is inherited synthetic structure, not CALPHAD. |
| Fe-rich solid at solidus + 1 K → primary nucleants | **This is not a valid identification of primary particles.** Near the solidus, most alpha has already formed; a second phase present then may have appeared after alpha and cannot automatically be credited with nucleating it. In **155 rows**, the counted Fe-rich phase coexists with more than 50% alpha; **146 rows** have a counted Fe-rich phase without an Fe-rich primary label. Phase presence also supplies no particle number density, size or nucleation potency. |
| Alpha composition → conductivity | Matthiessen plus Wiedemann–Franz is a defensible approximate transport model. But room-temperature dilute-solute resistivity coefficients are not validated high-temperature, multiphase DED transport properties. |
| Conductivity → lack-of-fusion power | Qualitatively sensible direction, but the proportional threshold is unvalidated. It omits absorptivity, beam size, powder capture/feed, latent heat, travel-speed coupling and temperature-dependent properties. The code does give **h = 0.355** for Cu–2.5Ni, but that does not establish that a real power cap ceases to bind there. |
| Equilibrium fractions → strength | A handbook-scale surrogate, not a calibrated yield-strength prediction. `600*sqrt(f)` is not an Orowan calculation without precipitate size/spacing. |

The supplied grid contains **31 points without alpha at 900 °C** and eight at 700 °C. The loader silently replaces missing alpha composition with nominal bulk composition. This avoids NaNs, but is not a physical alpha-matrix prediction; interpolating across that fallback can introduce artificial behavior.

### Specific code and feasibility issues

1. **Wrong reference state for the stated test.** `reference_m_for()` maximizes simulated deposit density, rather than using a dense wrought coupon. Its porosity multiplier makes the C71500 bar **9.23% more permissive in mass loss** than the corresponding fully dense model coupon; C70600 is **2.24%** more permissive.
2. **No coordinate-domain validation.** `wt_of()` clamps composition before feasibility checking. I verified that negative normalized Ni, `P = 2, v = -1`, and a process coordinate `a = 3` can all be accepted by `feasible()`. A standalone feasibility function should reject nonfinite/out-of-box coordinates before converting them.
3. **The stated composition rules are implemented as written for valid inputs.** Cu ≥65%, liquidus ≤1250 °C, Ni ≥Fe above 7% Al, and Fe ≤2.3% below 1.5% Al are correctly translated. The sharp boundaries are policy constraints, not phase boundaries. I could not verify their provenance in the absent proposal.
4. **No density or crack-screen feasibility requirement.** `F_SAFE = 0.50` is unused in this file. The 125 K screen is not enforced by `TP.feasible()`. Neither is minimum density, immersion pass, or minimum utility. Some may be enforced elsewhere, but that integration code was not uploaded.
5. **A soft objective gate is not a pass constraint.** An alloy may fail immersion and still have positive J. Indeed, the v1 optimum has positive J under the C70600 bar while failing the tabulated immersion threshold.
6. **The apparent porosity/beta trade-off can reward non-deposits.** Density can approach zero, corrosion grows by at most a factor of two, and high power/low travel suppresses beta. This produced the pathological 700 °C-feature solutions described above.
7. **Reference compositions are slightly inconsistent.** The normalized reference represents C70600 as **9.990Ni–1.395Fe–0.8Mn**, whereas the check/calibration composition is **10Ni–1.4Fe–0.8Mn**. Small numerically, but unnecessary for a defining comparator.
8. **Unit typo:** the `M_lo` comment says 1 µA·day/cm² is about **0.3 µm Cu**. With the code’s divalent-Cu convention it is **0.0318 µm**, a factor of ten smaller. The annual-rate conversion used in the tables is broadly consistent with divalent Cu; the comment is not.

## 3. README: what matches and what needs correction

Most saved-table arithmetic reproduces, including the dense beta-free ratios, reference-alloy properties, feasible-space share, random-design pass fractions, expected best-of-24 values, and J optima **0.0891/0.1900 near 15Ni–3Al–1.5Fe**. The important mismatches and unsupported numerical interpretations are:

| Statement | Audit result |
|---|---|
| “Lowest Ni that passes” **14.6/9.2 wt%** | Correct as **observed random-sample minima**, incorrect as landscape floors. Supplied-truth numerical floors are approximately **12.50/6.40**. |
| “Dense 70–30” reference | Actually **rho = 0.908**; C70600 is **0.978**. Fully dense reference bars give **15.97/6.97** in the otherwise unchanged model. |
| 30-day C70600/C71500 measured ratio **0.95** | Duplicate-mean ratio is **0.9686**: `(93.9+84.9)/(95.1+89.5)`. |
| Yang 2018: model is **28% above** C70600 in the **10-day** comparison | **1.286 is the 30-day model ratio** using the code’s usual C70600 chemistry. At ten days that ratio is **1.135**. |
| Yang 2018 comparator | The paper identifies its commercial comparator as **Cu–10Ni–1Fe–1Mn**, not the code’s 10Ni–1.4Fe–0.8Mn. With the paper’s chemistry, the original model ratio is approximately **1.025 at ten days**, versus measured **0.599**. The contradiction remains, but is smaller and differently defined. |
| Adding Yang leaves “the rest within 10%” | In the fit matching the README’s assumed comparator, `a_ni0` increases approximately **19.8%**. Its reported `a_al ≈ 0.17` and predicted ratio ≈1.02 are reproducible for that comparator assumption. |
| Conductivity “within 20%” | **Electrical** conductivity predictions meet that claim for the four listed grades. If interpreted as thermal conductivity, C71500 is **23.0 versus CDA 29.4 W/m·K**, approximately **21.7% low**. |
| NAB liquidus **51 °C high** | The supplied NAB composition predicts **1115.7 °C**. The CDA-derived Concast value I retrieved is **1060 °C**, implying approximately **56 °C high**. The 51 °C comparison cannot be traced to a specified reference value in this folder. |
| Equilibrium scan “1000, 950, …, 600 °C” | The actual list skips **650 °C**. |
| Finer grid moves optimum by “up to half a step” | No demonstrated error bound supports that statement. A finer grid can alter interpolated phase boundaries and rankings beyond half a current step. |
| “Measurements say” not to search below 10–15% Ni | Not supported. This is a conclusion of selected surrogate assumptions, contradicted as a robust restriction by the sensitivity results. |

There are also documentation inconsistencies within `truth_phys.py`: its introduction says a three-day film time while CAL uses ten days, and a comment gives C71500’s Scheil range as 167 K whereas the tabulated reference is approximately 162 K.

For the handbook comparisons I used the Copper Development Association records for [C71500](https://alloys.copper.org/alloy/C71500?referrer=facetedsearch), [C70600](https://alloys.copper.org/alloy/C70600?referrer=facetedsearch), [C61400](https://alloys.copper.org/alloy/C61400?referrer=facetedsearch), and the [Concast C95800 sheet](https://www.concast.com/files/C95800.pdf). Full BibTeX entries are saved with the audit citations.

## Recommendation and limitations

I would describe this as a **physics-informed synthetic truth with a sensitivity ensemble**, not a calibrated physical truth establishing a nickel cutoff. Before using it in the proposal, I would fix the reference state, replace random-sample minima with constrained floor searches, correct the Yang comparison, distinguish measured targets from transferred/prior targets, validate the candidate domain, and prevent near-zero-density designs from being treated as meaningful coupons.

For benchmark robustness, I would retain several alternative truths spanning Ni saturation, Al protection and matrix partitioning. The scientifically defensible conclusion is that **the supplied evidence does not establish a universal low-Ni exclusion threshold for the proposed 30-day test**—not that zero-Ni alloys have been shown to pass.

I could not rerun the thermodynamic calculations because the database and `run_calphad.py` helper were not supplied. I therefore could not verify database phase labeling, missing interaction parameters, phase-fraction basis, or equilibrium/Scheil solver settings beyond the visible wrapper and CSV. The original Popplewell full text was inaccessible; I checked its numerical rates as reproduced by Lewis and LaQue. I could not verify the absent synthetic truth, BO integration, seed generator, proposal constraints, external figures or stored BO runs. My searches also do not prove that no relevant experiment exists anywhere.

### Discretionary analytical decisions

- I compared **raw mass loss**, avoiding artificial passes caused by clipping the immersion index at one.
- I recomputed both reference bars for each refit, so parameter changes did not silently retain an incompatible original threshold.
- I optimized Ni directly, eliminating the process coordinate that maximizes `q` analytically, then using global search plus constrained local refinement. I split the Al regimes at the discontinuous feasibility boundaries and independently checked the original-truth witnesses.
- I treated alternate targets, weights and functional forms as **sensitivity scenarios**, not statistically interchangeable models or a confidence interval; source uncertainties and covariance are unavailable.
- I reported the deposited-reference convention separately from the requested dense-wrought convention, and imposed a density minimum only in explicitly labeled checks.
- I used the uploaded CSV rather than reconstructing unavailable thermodynamic dependencies, and explicitly omitted statistics requiring missing code.
