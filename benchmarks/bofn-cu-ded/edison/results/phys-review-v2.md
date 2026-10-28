# Follow-up review: does the refitted copper-alloy benchmark establish a nickel floor?

## Verdict

**No: I would not restrict the search to Ni ≥10 wt%.** The new copper anchors support a protective effect of nickel in several tested environments, but they do not establish a universal minimum Ni content for Cu–Ni–Al–Fe–Mn deposited by directed energy deposition (DED), particularly at **30 days**. There is still no measured 0–10 wt% Ni composition series that separates Ni from Al, Fe, microstructure and exposure history.

My independent base refit gives globally optimized **film-only** floors of **1.509 wt% Ni against C70600 (90–10)** and **2.500 wt% against C71500 (70–30)**, not 10 wt%. Changing quadratic Al to linear Al raises those numbers to **10 and 30 wt%**, respectively. That is the largest single model-form effect in the requested sensitivities. These are conditional model boundaries, **not experimentally established exclusion limits or confidence bounds**.

In the supplied full truth, I independently find feasible deposited-alloy boundary solutions at **2.205 and 3.264 wt% Ni**. These are multistart local optimization results, not certified global minima. More decisively, an executed witness with **Ni 5.000, Al 2.907, Fe 3.942, Mn 0, Cu 88.151 wt%** has immersion index **0.88113**, above both implemented bars (**0.81049 and 0.84207**), and satisfies every search-space limit. A Ni ≥10 restriction therefore discards passing alloys **even under the benchmark's own truth**.

**Use dense C70600 as the primary meaning of “no worse than the reference,” because that is the stated default.** Report C71500 as a separate, explicitly stricter requirement—not as a retrospective replacement chosen to obtain a desired floor. Both references must be tested alongside candidates under the actual 30-day protocol.

## 1. Severity-ranked findings

| Severity | Finding | Consequence | Evidence/check status |
|---|---|---|---|
| **Changes the conclusion** | The Al response controls whether a low-Ni route exists: quadratic versus linear Al changes floors from 1.509/2.500 to 10/30 wt% Ni. | A universal Ni floor, especially 10 wt%, is not robust to defensible functional forms. | **Executed:** independent refits and continuous optimization. |
| **Changes the conclusion** | Strict exclusions leave the Al response unidentified: the nine-row exposure-rate subset has within-study feature rank 3, and removing the 10-day Yang pair leaves rank 2 of 4. | Numerically generated floors of 0/0 or 10/30 in those subsets reflect ridge extrapolation or zero-filled coefficients, not evidence resolving the floor. | **Executed:** exclusions, rank checks, refits, optimized witnesses. |
| **Changes the conclusion** | None of the 14 additions measures 30-day low-Ni DED performance; several are hot brine, deep ocean or localized-loss tests. | Same-test ratios cannot by themselves transport alloy effects to 30-day ambient immersion. | **Inspected:** primary/compilation tables for 12 rows; uploaded anchor only for the last two. |
| **Changes the conclusion** | The full truth admits a clear 5 wt% Ni passing witness. Its Ni ~12 wt% objective optimum also rewards strength, processability and mineral burden. | Neither that objective optimum nor the sampled passing fraction establishes a minimum Ni requirement. | **Executed:** witness, feasibility and optimum-point evaluation; global objective search not repeated. |
| **Changes a number** | The shipped “floor” routine uses a 0.1 wt% grid, not continuous optimization. | Its base 1.6/2.6 becomes 1.509/2.500; its first passing witness is not the optimal Al witness. | **Inspected:** routine; **executed:** independent optimization. |
| **Changes a number** | “Dense” truth references are actually optimized DED references with density indices 0.98024/0.97356. | Their porosity penalties relax the bar relative to truly dense references; corrected full-truth local boundaries are 2.387/3.569 wt% Ni. | **Executed:** reference calculation and constrained reoptimization. |
| **Changes a number** | The full-truth boundary witnesses in the upload are not minima I recover. | Their 2.246/3.293 wt% becomes 2.205/3.264 with slightly better process/composition choices. | **Executed:** six-start constrained optimization in the middle-Al branch. |
| **Changes a number** | Two matched Wheatfall exposure pairs in the anchor were omitted, including the 1,064-day pair where copper has lower loss. | Including both changes film floors to 1.109/2.016; the additions should not be presented as exhaustive evidence. | **Inspected:** Tables 34–35; **executed:** added-pair sensitivity. |
| **Changes a number** | Nominal/assumed compositions, electrochemical proxies, generic bronze assignments and hand-written penalties are treated as if they determine physical rate ratios. | Numerical precision overstates calibration quality; model-form and composition uncertainty dominate. | **Inspected:** data and equations; **executed:** exclusions and penalty sensitivities. |
| **Changes a number** | Mn =0 does not generally minimize grid liquidus, contrary to the fitting helper's comment. | It is not a valid general reduction of the feasible domain. It does not alter my film floors because each unrestricted lower-bound witness is already feasible at Mn =0. | **Executed:** grid-node comparisons and witness feasibility. |
| **Cosmetic / reproducibility** | The uploaded files are flat, but `truth_phys.py` expects `phys/`; reference compositions in the fitter and truth differ slightly. Ravindran has a publisher-listed DOI absent from the anchor. | Fix packaging and use one reference-composition definition. The DOI endpoint returned 404, so I saved verified publisher metadata instead. | **Executed:** path-only overrides, composition comparison, metadata retrieval. |

## 2. Audit of the 14 added rows

CSV line numbers below include the header. I checked **all 14 against `copper-anchor.md`**. The numerical rates agree with it. Agreement with that narrative is not independent source verification; I distinguish that explicitly below. The nominal/assumed composition columns are not equivalent to measured specimen chemistry.

| CSV lines / rows | Source comparison | Assessment and appropriate use | Check performed |
|---|---|---|---|
| **18–20:** Cu 61.0; 90–10 22.5; 70–30 22.5 µm/y | Ravindran 1983, Table 5, PDF p.5 / printed p.94 [R1]. All three panels shared 120 days at Cochin Harbour, with tidal flushing, still to 0.80 m/s. | **Fair internally matched field comparison**, not quiet 30-day immersion. The method for Table 5 is not explicitly established as weight loss. Ni 10/30 is nominal; the CSV's Fe 1.4/0.6 and Mn 0.8/0.6 are assumptions, not Table 5 assays. Do not confuse the paper's separately discussed weight-loss curves with confirmation of this table's method. | **Primary PDF inspected; rates verified.** |
| **21–22:** Cu 12.1; Cu–30Ni 6.27 mdd | Wheatfall 1967 via Gdowski 1991, Tables 34–35, PDF p.45 / printed p.40 [R2]. Matched 123-day exposure at 5,640 ft, 2.78°C, ~2,500 psi, dissolved O₂ 1.19 ppm. | **Fair same-exposure mass-loss pair, weak target-domain anchor.** Cold, low-oxygen deep ocean is not ambient surface immersion. Cu–Ni Fe/Mn are assumed. | **Compilation inspected; original Wheatfall experiment not retrieved.** |
| **23–24:** Cu 4.50; Cu–30Ni 1.42 mdd | Same tables [R2]; surface, 386 days, 17.61°C, 1–2 knots. Footnote b explicitly attributes the copper loss largely to localized corrosion. | **Matched exposure, but not a fair uniform-film-rate calibration.** It can inform a localized-damage endpoint, provided that endpoint is separately defined. Drop the pair from a uniform-film sensitivity—not just the copper row, which would leave no within-block contrast. | **Compilation inspected; footnote verified.** |
| **25–29:** C122 0.99; C608 0.75; C613 0.73; C706 0.70; C715 0.46 mpy | Cohen–Whitted 1971 via Banning–Oden 1973, Tables 7–8, PDF pp.18–19 / printed pp.14–15 [R3]. These are genuinely the same **4 ft/s, 697-day** column. | **Fair same-loop comparison, not fair direct transport to the target test.** Temperature 250°F (~121°C), 83% normal seawater salinity, treated oxygen-poor brine, 72 ppb O₂ in makeup. Table 7 gives specification maxima/ranges, not assays. C608 Al 5.75 and Fe 0.05 are assumed representatives; C613 Al 7 and especially Fe 2.5 are not measured values. C613's specified 0.2–0.5% Sn is omitted from the model. C715 Ni 31 and Fe 0.55 represent ranges, not measured chemistry. | **Compilation PDF inspected; all five rates and column match verified. Original Corrosion/71 paper not retrieved.** |
| **30–31:** 90–10 0.145; 70–30 0.067 mpy | Al-Fozan–Malik 2008, Tables 1 and 3, as transcribed in the anchor [R4]. Nominally same immersion conditions, but **198 versus 192 days**. | **Not an exact same-duration pair.** The measured compositions in the CSV agree with the anchor; the nearby durations make this a reasonable qualified sensitivity input, not a 30-day measurement. It adds a 10-versus-30 comparison, not a low-Ni anchor. | **Anchor inspected only for numbers.** DOI metadata retrieved; full-text retrieval failed/was blocked or returned metadata only. I did **not** independently verify its tables. |

**Omitted evidence:** Gdowski also reports Cu/Cu–30Ni **3.78/2.75 mdd at 751 days** and **2.65/3.08 mdd at 1,064 days**. The latter reverses the copper-versus-Cu–Ni ordering. I added both as separate exposure blocks in a sensitivity, not as extra independent studies. The uploaded “11 studies” are actually **11 fitted blocks**, with Wheatfall split by exposure and Lewis–LaQue appearing twice; that is not 11 wholly independent sources.

**Older-row issue relevant to this refit:** Lewis–LaQue Table XIV [R5] really reports uncoupled aluminum bronze **43.2**, nickel aluminum bronze **150.0**, C70600 **30.5** and C71500 **20.3 µm/y** after one year at 0.6 m/s. I verified those values, but the table does **not** establish the particular C61400/C95800 compositions assigned in the CSV. Those assumed compositions are consequential Al-response inputs, not measured low-Ni bronze chemistry.

## 3. Independent refit and optimized floors

### Method and verification

I wrote and executed my own fitting code **before calling the supplied fitter**. I eliminated each study/exposure intercept by **weighted within-block centering**, then solved the bounded ridge regression on the four composition features. This is an independent implementation of the stated weighted least-squares objective, not a fit to the supplied coefficients.

For the base case, with Al² divided by 10:

\[
(b_{Ni},b_{Al},b_{Al2},b_{Fe})
=(-0.840921,-0.279938,+0.385670,\;\text{approximately }0).
\]

Unweighted residual root-mean-square error (RMSE) is **0.226696 in ln(rate)** for 30 rates. The independent coefficients match the subsequently executed supplied fit function to **2.84×10⁻¹¹** maximum absolute difference. This confirms implementation agreement, not physical validity. In particular, the protective Fe coefficient is on its imposed zero boundary; the unconstrained fit instead estimates **+0.12880**. Freeing signs is a diagnostic of confounding/model inadequacy, not proof that Fe is intrinsically harmful.

I minimized Ni continuously over Ni 0–30, Al 0–9.5 and Fe 0–4.5 wt%, with Cu ≥65%, the two conditional composition rules and interpolated liquidus ≤1,250°C. For the film model, I first obtained the exact unrestricted lower bound by minimizing the separable Al and Fe contributions and solving the Ni constraint. **Every one of the 32 fits below attains that lower bound at a feasible witness with Mn =0.** Thus these film-model floors are globally certified for the stated deterministic model, not simply grid hits or local minima. Allowing Mn to vary cannot beat an already attained unrestricted lower bound.

All witnesses have Cu as the balance. The table gives common witness Al/Fe for both bars; combine those columns with the corresponding Ni floor and Mn =0. Values are rounded for display; exact feasible compositions and residual margins are in `optimized_witnesses.csv`. Film comparisons use the supplied fitter's reference compositions **(Ni,Al,Fe) =(10,0,1.4)** and **(30,0,0.6)**.

| Independent refit | n | RMSE ln | Ni floor: 90–10 | Ni floor: 70–30 | Witness Al | Witness Fe |
|---|---:|---:|---:|---:|---:|---:|
| Base | 30 | 0.227 | 1.509 | 2.500 | 3.629 | 0.000 |
| Linear Al | 30 | 0.323 | 10.000 | 30.000 | 0.000 | 0.000 |
| Signs free | 30 | 0.223 | 0.406 | 1.956 | 3.752 | 0.000 |
| Linear Al, signs free | 30 | 0.320 | 4.603 | 10.807 | 0.000 | 0.000 |
| Ni scale 3 | 30 | 0.249 | 1.150 | 1.311 | 3.501 | 0.000 |
| Ni scale 8 | 30 | 0.204 | 1.355 | 4.341 | 3.691 | 0.000 |
| Ni scale 12 | 30 | 0.193 | 0.669 | 5.787 | 3.650 | 1.500 |
| Linear Ni | 30 | 0.184 | 0.000 | 7.822 | 3.418 | 1.500 |
| Fe cap 1.0 | 30 | 0.227 | 1.509 | 2.500 | 3.629 | 0.000 |
| Fe cap 2.5 | 30 | 0.227 | 1.509 | 2.500 | 3.629 | 0.000 |
| No ridge | 30 | 0.227 | 1.496 | 2.484 | 3.666 | 0.000 |
| Ridge 0.5 | 30 | 0.234 | 1.659 | 2.683 | 3.340 | 0.000 |
| Equal row weights | 30 | 0.224 | 0.918 | 1.787 | 3.569 | 0.000 |
| Drop AlFozan2008 | 28 | 0.217 | 1.459 | 2.438 | 3.601 | 0.000 |
| Drop CohenWhitted1971 | 25 | 0.226 | 2.896 | 4.249 | 3.281 | 0.000 |
| Drop LewisLaQue1981_1y | 26 | 0.163 | 1.109 | 2.016 | 4.635 | 0.000 |
| Drop LewisLaQue1981_quiet | 28 | 0.234 | 1.518 | 2.510 | 3.634 | 0.000 |
| Drop Qian2025 | 28 | 0.223 | 1.479 | 2.462 | 3.612 | 0.000 |
| Drop Ravindran1983 | 27 | 0.234 | 1.258 | 2.195 | 3.503 | 0.000 |
| Drop Tan2024 | 26 | 0.205 | 0.000 | 0.568 | 3.613 | 0.000 |
| Drop Wheatfall1967_123d | 28 | 0.233 | 1.566 | 2.569 | 3.663 | 0.000 |
| Drop Wheatfall1967_surface | 28 | 0.229 | 1.400 | 2.367 | 3.570 | 0.000 |
| Drop Yang2018 | 28 | 0.235 | 1.816 | 2.876 | 3.555 | 0.000 |
| Drop Zhao2022 | 28 | 0.223 | 1.308 | 2.255 | 3.599 | 0.000 |
| Drop hot brine + deep/localized Wheatfall | 21 | 0.240 | 2.889 | 4.240 | 3.275 | 0.000 |
| Drop unspecified bronze rows | 28 | 0.161 | 1.119 | 2.028 | 4.644 | 0.000 |
| Previous exclusions + unspecified bronzes + Zhao | 17 | 0.163 | 1.190 | 2.113 | 4.734 | 0.000 |
| Weight each study equally | 30 | 0.225 | 1.403 | 2.370 | 3.577 | 0.000 |
| Add omitted 751d + 1064d Wheatfall blocks | 34 | 0.242 | 1.109 | 2.016 | 3.442 | 0.000 |
| Drop all Wheatfall exposures | 26 | 0.238 | 1.455 | 2.433 | 3.599 | 0.000 |
| Exposure rates only, conservative exclusions† | 9 | 0.165 | 0.000 | 0.000 | 9.500 | 0.000 |
| Same exclusions, also drop 10-day Yang† | 7 | 0.187 | 10.000 | 30.000 | 0.000 | 0.000 |

† **Do not interpret the last two rows as well-identified alternatives.** The nine-row subset retains Yang, the two Lewis–LaQue Cu–Ni rows, Ravindran and Al-Fozan. Its sole Al contrast is the **10-day Yang** pair; linear and quadratic Al are not separately identifiable. Ridge selects an extrapolated high-Al optimum, giving zero-Ni witnesses at Al 9.5. Without Yang, no Al contrast remains at all; ridge sets both Al coefficients to zero and recovers 10/30 by construction. These rows expose an evidence gap, not a credible measured 0% or 10% cutoff.

### What moves the floor?

- **Largest requested single model-form change: Al linear versus quadratic.** Floors shift **+8.491 and +27.500 wt% Ni** from the base case. In the quadratic base fit, Al **3.629 wt%** lowers log rate by **0.508**, a rate multiplier of **0.602**. This inferred benefit opens the low-Ni route; it is not directly measured in a 30-day low-Ni series.
- **Ni response shape matters**, especially for the stricter bar: scales 3/5/8/12 give 70–30 floors **1.311/2.500/4.341/5.787**; linear Ni gives **7.822**. Linear Ni has lower training RMSE (**0.184 versus 0.227**), so the data do not select the assumed 5 wt% saturation scale by fit quality. Training RMSE alone is not model validation.
- **Signs matter:** freeing them lowers the quadratic floors to **0.406/1.956**; linear Al with free signs gives **4.603/10.807**. The newly anchored free-sign fits do not make Ni harmful; the earlier behavior is not reproduced here.
- **Study selection matters but does not recover a robust 10% rule.** Dropping hot brine raises floors to **2.896/4.249**; dropping Tan lowers them to **0/0.568**. Those are the largest leave-one-block shifts for the 70–30 bar. Dropping all hot/deep/localized additions gives **2.889/4.240**.
- **Weights and weak ridge are smaller effects here.** Equal row weights give **0.918/1.787**; equal total weight per fitted block gives **1.403/2.370**. Removing or strengthening ridge changes floors by <0.19 wt% from base. Fe-cap changes have no effect in the constrained base fit because its Fe coefficient is zero.

These are **sensitivity envelopes, not statistical confidence intervals**. There are too few comparable independent tests, and too much uncertain chemistry and endpoint mixing, to attach an honest narrow confidence interval to a physical floor.

## 4. Immersion physics and use inside the truth

### Executed full-truth checks

I ran `PhysTruth` after overriding **only its two input paths in memory**, because the uploaded layout is flat. I did not edit any uploaded input. I reproduced both implemented reference indices and the uploaded floor witnesses. I then minimized Ni with six-start constrained sequential least-squares programming over composition and the three process settings, in the **1.5–7 wt% Al branch**. All six starts converged to the same reported boundary within numerical tolerance. Other branches/global optimality were **not certified**.

| Reference convention | Bar | Best Ni found | Al | Fe | Mn | Density index | Beta index |
|---|---|---:|---:|---:|---:|---:|---:|
| Implemented best-DED reference | C70600 | 2.205 | 2.907 | 3.942 | 0 | 0.98523 | 0.10758 |
| Implemented best-DED reference | C71500 | 3.264 | 2.913 | 3.984 | 0 | 0.98632 | 0.10639 |
| Ideal dense reference, candidate still DED | C70600 | 2.387 | — | — | — | — | — |
| Ideal dense reference, candidate still DED | C71500 | 3.569 | — | — | — | — | — |

Exact compositions/process settings for every row are saved in `full_truth_optimizations.json`. Threshold equalities are numerical, not experimental pass margins. The separate **5 wt% Ni witness in the verdict** has a clear positive margin instead.

The ideal dense-reference indices are **0.816415/0.850000**, versus the implemented **0.810487/0.842067**. The model currently calls a porosity-penalized deposited reference “dense.” Also, `bofn_alloy.REFERENCE` actually decodes to C70600 **Ni 9.99, Fe 1.395, Mn 0.8** and C71500 **Ni 30, Fe 0.675, Mn 0.8**, not exactly the fitter's reference compositions. This discrepancy is small for the base fit, where Fe has zero effect, but should be removed before sensitivity comparisons.

Keeping the implemented bar fixed while changing **candidate-only** hand-written immersion penalties gives:

| Candidate penalty sensitivity | Ni floor found, 90–10 | Ni floor found, 70–30 |
|---|---:|---:|
| Baseline | 2.205 | 3.264 |
| No beta-prime penalty | 1.442 | 2.348 |
| Twice beta-prime penalty | 2.712 | 3.892 |
| No porosity penalty | 1.358 | 2.255 |
| Twice porosity penalty | 2.323 | 3.397 |

This is a perturbation diagnostic, **not a refit or recalibration of reference bars**.

### Physically misleading assumptions

1. **No 30-day kinetic model.** Study intercepts remove absolute levels and units, not alloy-by-time, temperature, oxygen, flow or salinity interactions. Rates from 7-day impedance, 10-day mass loss, 30-day polarization and up to 697-day brine exposure cannot automatically share a transferable 30-day alloy response. The model predicts relative surrogate rates; it has not calibrated an absolute 30-day mass loss.
2. **Mixed observables are not interchangeable rates.** A polarization current or inverse charge-transfer resistance can have alloy-dependent conversion factors and localized-attack sensitivity. A study intercept does not remove these within-study differences. Midpoints of broad literature rate ranges also are not a matched exposure experiment.
3. **Film coefficients and signs are assumptions, not a floor mechanism.** Saturating Ni at a fixed 5 wt% scale, clipping Fe at 1.5 wt%, and requiring nonpositive Ni/Fe slopes encode prior beliefs. `min(nominal Fe,1.5)` is not measured or CALPHAD-derived **Fe in solution**. Mn, missing minor elements and microstructure are omitted from immersion chemistry.
4. **The Al quadratic conflates film chemistry and microstructure.** The source mixtures already contain cast/duplex/laser-deposited alloys with their actual phases and defects. Adding a separate hand-written beta-prime penalty risks double-counting selective attack. It is particularly misleading to read the beta index as a phase fraction: the formula produces ~0.108 at only ~2.9 wt% Al without any phase-existence check, and it is not tied to the supplied CALPHAD beta field. This is a synthetic index, not demonstrated retained beta-prime in those witnesses.
5. **Porosity treatment is not fitted corrosion physics.** A linear penalty in `1−rho_m` cannot represent connected versus closed pores, crevices, exposed area or localized penetration. The “density” node also combines process window and cracking into an index, so it is not an independently measured pore-volume fraction. Translating the penalty into log-rate units does not validate it.
6. **Implementation choices affect benchmark conclusions.** The immersion output is clipped to [0,1], so different rates can collapse to the same index near saturation. The objective uses a **soft sigmoid gate**, not a hard pass requirement; an objective optimum is not the minimum-Ni passing alloy. The one-hour screen is hand-written and ignored by the actual immersion truth despite being a parent input to its learned surrogate. Any claimed screen/immersion discrepancy remains partly designed into the benchmark.
7. **CALPHAD is not validation of DED phase selection.** I inspected/interpolated the supplied grid, not reran pycalphad or validated the database. Equilibrium fields and multilinear interpolation do not establish retained phases in rapidly cooled, segregated DED material. All 864 rows have `ok=1`; 33 missing liquidus entries are replaced in the truth with 1,550°C scan-bound values, which are not measured liquidus temperatures. None of my low-floor witnesses is near that substitution region or the 1,250°C limit.

The benchmark can still be useful as a **documented synthetic stress test**. It should not be described as experimentally established physical truth that excludes low-Ni alloy families.

## 5. Smallest discriminating experiment

**To test the proposed Ni ≥10 restriction, the smallest useful falsification experiment is one low-Ni candidate plus both references:**

- DED **Cu–5Ni–3Al–1.5Fe**, Mn nominally zero, Cu balance **90.5 wt%**. This tests the predicted Al-assisted low-Ni route, not pure Cu–Ni extrapolation.
- Dense, assayed **C70600** and **C71500**, separately identified as the default and stricter comparators.
- Start with **three independently deposited candidate specimens** and three independent specimens of each reference: **nine coupons**. This is a minimum screening design, **not a power-justified noninferiority trial**. Independently deposited specimens/build positions matter; repeatedly weighing one coupon is not replication.

**To distinguish a ~0%, ~2–3% and ≥5% transition, add Cu–0Ni–3Al–1.5Fe and Cu–2.5Ni–3Al–1.5Fe**, with the same replication: **five alloy groups, 15 coupons**. These three candidate compositions all satisfy the computational search limits. An optional unalloyed-copper group is a useful process/chemistry sentinel but is not essential to the first falsification.

Use **30 days of simultaneous, fully submerged, electrically isolated immersion** in one specified seawater batch/protocol, preferably clean aerated natural seawater at **25 ±2°C** with controlled gentle circulation (or explicitly specified static immersion), measured dissolved oxygen, salinity and pH. Match exposed area and final surface finish; control/record renewal, film preconditioning and edge/crevice geometry. Use an appropriate standardized immersion/cleaning procedure, cleaning blanks and area-normalized mass loss, plus maximum pit depth and cross-sectional selective attack. Assay Ni/Al/Fe/Mn, characterize phases and connected porosity, and confirm the low-Ni deposits are not diluted substrate mixtures.

Pre-register what “no worse” means: the **30-day cumulative mass-loss ratio to C70600**, with C71500 secondary, and a separate localized-damage requirement. For a literal ratio ≤1 criterion, evaluate a prespecified one-sided upper confidence bound; with only three replicates it may be inconclusive. Set a practically acceptable noninferiority margin *before* seeing results if literal equality is experimentally unrealistic, and then increase replication based on pilot variability. A passing 5% alloy falsifies a universal ≥10% floor; a failed alloy does **not** prove one. No finite small experiment proves that every lower-Ni composition fails. A 90-day follow-on is useful for film maturation, but should not replace the specified 30-day decision.

## 6. What I executed versus only inspected

| Check | Status |
|---|---|
| Independent base and 31 alternative refits; continuous film-floor optimization; full witness feasibility | **Executed**, with exact lower-bound attainment certificates for the deterministic film model. |
| Supplied `fit_corrosion.fit` coefficient comparison | **Executed after my implementation**. Supplied `main()` and its gridded floor calculation were **inspected, not rerun**. |
| All 14 additions against uploaded anchor | **Inspected all rows**; 12 values additionally checked in directly accessible primary/compilation tables; Al-Fozan's two table values **not independently source-verified**. |
| Full-truth reference calculation, uploaded witnesses and optimum point, new multistart floor searches, dense-bar and penalty sensitivities | **Executed**. Full-truth global minima and the uploaded global objective optimum **not independently certified**. |
| Uploaded 5.2%/3.2% passing shares | **Inspected only**, not resampled; these depend on the sampling distribution, not just the alloy domain. |
| CALPHAD grid completeness, liquidus interpolation and Mn dependence | **Executed grid checks**. Underlying thermodynamic calculations/database and real DED phases **not validated**. |
| Reproduction scripts | **Both executed successfully in fresh Python subprocesses**; reproduced recorded floor values exactly in this environment. No experimental work performed. |

## 7. Files and sources

Saved alongside this report:

- `refits.csv`, `refits.json`: coefficients, fit errors and optimized floors for all 32 scenarios.
- `optimized_witnesses.csv`: full Ni/Al/Fe/Mn/Cu witnesses, liquidus and rate/feasibility margins for both bars.
- `new_rows_audit.csv`: all 14 row-level provenance checks and qualifications.
- `full_truth_optimizations.json`: exact composition/process witnesses and penalty/dense-reference sensitivities.
- `reproduce_refits.py`, `reproduce_full_truth.py`, `environment.json`, `execution_checklist.json`; downloaded/parsed evidence in `sources/`. Uploaded inputs remain unchanged.

Reproduce from `/workspace`:

```bash
python outputs/reproduce_refits.py
python outputs/reproduce_full_truth.py
```

The second script requires PyTorch and BoTorch; exact installed versions are recorded. Source retrieval need not be repeated for the numerical reproduction.

**Source references** — full BibTeX records are saved in the [verified bibliography](../citations/local-copper-review/e8550274-e07d-4d00-9af7-1a2a7d7da0c0-verified.bib).

- **[R1; `ravindran1983marine`]** K. Ravindran (1983), “Copper-Nickel Alloys for Marine Aquacultural Engineering,” *Fishery Technology* **20**(2), 90–96, Table 5. [Primary PDF](https://epubs.icar.org.in/index.php/FT/article/download/70952/60283/468475). Publisher-listed DOI **10.56093/ft.v20i2.70952**; resolver returned 404 during this review.
- **[R2; `gdowski1991degradation`]** G. E. Gdowski (1991), *Survey of Degradation Modes of Four Nickel-Chromium-Molybdenum Alloys*, Tables 34–35, compiling Wheatfall (1967). DOI: [10.2172/138275](https://doi.org/10.2172/138275).
- **[R3; `banning1973hotbrines`]** L. H. Banning and L. L. Oden (1973), *Corrosion Resistance of Metals in Hot Brines: A Literature Review*, U.S. Bureau of Mines IC 8601, Tables 7–8, compiling Cohen and Whitted, Corrosion/71 Paper 57. [Compilation PDF](https://stacks.cdc.gov/view/cdc/235753/cdc_235753_DS1.pdf).
- **[R4; `Al_Fozan_2008`]** S. A. Al-Fozan and A. U. Malik (2008), “Effect of seawater level on corrosion behavior of different alloys,” *Desalination* **228**, 61–67. DOI: [10.1016/j.desal.2007.08.007](https://doi.org/10.1016/j.desal.2007.08.007). Numerical table claims here are attributed to the uploaded anchor, **not independently retrieved full text**.
- **[R5; `Lewis_1981`]** R. O. Lewis and F. LaQue (1981), *Evaluation of Copper-Nickel Alloys for OTEC Applications*, Table XIV, compiling “Inco Unpublished Data.” DOI: [10.2172/6255887](https://doi.org/10.2172/6255887).

## Discretionary analytical decisions

- I retained the supplied log-rate/ridge objective and weights for the base case, so the first check isolates implementation correctness rather than silently changing the model.
- I used exact separable optimization with feasibility verification instead of a denser Ni grid; it certifies the film-model floors without grid-rounding ambiguity.
- I removed entire two-row exposure blocks when their comparisons were weak, and retained the two source-reported omitted Wheatfall pairs in a separate sensitivity. I did not select only favorable copper-anchor results.
- I separated plausible model-form sensitivities from rank-deficient strict-data fits, and did not treat synthetic sensitivity ranges as physical confidence intervals.
- I kept C70600 primary, C71500 secondary, and distinguished ideal dense references from optimized deposited references. I labeled full-truth searches as local rather than claiming a global result I did not establish.
- I recommended the smallest falsification study separately from a larger transition-mapping study; neither can prove a universal minimum over an alloy continuum.