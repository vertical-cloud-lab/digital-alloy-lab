# Independent review: no defensible universal nickel floor

[**Download the complete Markdown report**](data_entry:report-md-eyq7) · [Supporting evidence, numeric tables and runnable code](data_entry:review-supporting-files-zip-nogw)

I saved the complete report at **`/workspace/outputs/report.md`**. It contains the 16-row source audit, severity-tagged findings, all **82 optimized floors with witnesses**, full-network checks, CALPHAD spot checks, limitations and experiment design.

## Verdict

**The evidence does not establish a robust positive nickel floor, and I would not restrict the search to Ni ≥ 10 wt%.** The physics-based truth is defensible as an explicitly qualified **what-if simulator**, not as validated prediction of 30-day seawater performance.

My independent implementation reproduces the base fitting coefficients to within \(1.1\times10^{-15}\). Continuous optimization gives film-only floors of **0.947 wt% Ni against 90–10** and **1.822 wt% against 70–30**. In the full network, I verified strictly passing, feasible witnesses at **1.6250** and **2.4312 wt% Ni**, respectively.

Those are synthetic-model results—not experimentally demonstrated alloy limits.

## Principal findings

| Severity | Finding | Consequence |
|---|---|---|
| **Changes the conclusion** | The floor changes substantially with Ni response, Al response and evidence exclusions. | Original-data alternatives span **0–5.471 wt% Ni** under 90–10 and **0–15.857** under 70–30. A strict but data-poor subset instead gives **10/30**. This is identification uncertainty, not justification for selecting a cutoff. |
| **Changes the conclusion** | The composition-resolved evidence is weaker than the table implies. | Lewis’s bronze grades are unspecified; their assigned chemistries are unsupported. Yang’s commercial comparator is incompletely documented. Zhao’s steel-diluted coatings confound composition with processing. |
| **Changes the conclusion** | The benchmark does not actually count tensile strength only after passing immersion. | Its logistic gate gives **50% strength credit at the bar**, and nonzero credit below it. A hard final pass/fail objective should be separate from a smooth acquisition utility. |
| **Changes the conclusion** | mc_ni is extrapolated far outside its documented validation domain. | Its header specifies **Cu < 0.5 wt%**; the search requires **Cu ≥ 65 wt%**. I verified the database hash and absence of explicit Cu–Al–Ni ternary parameters. |
| **Changes a number; potentially the conclusion** | A NAB-like near-solidus grid state does not match an independent equilibrium solve. | Stored liquid fraction **0.95730** versus independently calculated **0.08340**; the stated nucleant mapping changes from **g = 0.61 to 0**. The missing generator helper prevents attributing a single cause. |
| **Changes a number** | Qian’s entries are constructed inverse-resistance proxies, not measured penetration rates. | Replacing them with the same paper’s seven-day Tafel pair changes the floors to **1.597/2.607 wt% Ni**. |
| **Changes a number** | Quiet-water “rates” of 0.4/0.4 mpy are constructed midpoints. | The source reports ranges **0.2–0.6** and **0.3–0.5 mpy**, with unspecified duration. |

## A genuine missing copper comparison was recovered

I found a primary **same-deployment immersion comparison** in Reinhart’s 1968 report and checked the original scanned tables locally:

| Material | Actual Ni, wt% | Rate, mpy |
|---|---:|---:|
| Oxygen-free copper | 0 | 1.6 |
| Nominal “95–5” Cu–Ni | **6.25**, not 5 | 1.5 |
| 90–10 coupon | 9.42 | 1.6 |
| 70–30 coupon | 30.53 | 1.2 |

These measurements share a **123-day, 5,640-ft cold deep-seawater deployment**. They partly close the compositional gap, but do **not** validate transfer to 30-day warm surface seawater or DED material. Exact Cu–2Ni/Cu–5Ni target-test evidence remains missing.

Adding these four observations reduces the base film-only floors from **0.947/1.822** to **0.195/0.938 wt% Ni**. Adding the matched aluminum bronze gives **0/0**, although that bronze also showed selective attack—another reason not to equate average mass loss with adequate corrosion resistance.

## Selected independent optimized floors

All values are wt% Ni. The full report gives witnesses and coefficients for every fit.

| Fit or evidence change | 90–10 bar | 70–30 bar |
|---|---:|---:|
| Base: saturating Ni, quadratic Al, fixed protective signs | 0.947 | 1.822 |
| No ridge | 1.453 | 2.431 |
| Ni saturation scale 3 wt% | 0 | 0 |
| Ni saturation scale 8 wt% | 1.982 | 5.268 |
| Ni saturation scale 12 wt% | 1.591 | 7.771 |
| Linear Ni | 0 | 15.857 |
| Free signs | 0 | 0 |
| Add Mn | 0 | 0.388 |
| Add Ni × Al | 0 | 0 |
| Drop Yang comparison | 5.471 | 7.999 |
| Drop Zhao coatings | 0 | 0 |
| Add matched Cu/Cu–Ni immersion bridge | 0.195 | 0.938 |
| Strict subset plus bridge | 10.000 | 30.000 |

The strict subset returns reference-level floors after removing the principal low-Al benefit comparison. **That is not proof that lower-Ni Al-bearing alloys cannot pass.** Equally, zero predicted floors are not proof that pure copper passes the intended test.

## Executed versus inspected

- **Data:** retrieved and inspected full source text for all five documents underlying the original 16 rows; reconciled every original row. Lewis remains secondary evidence. Delegated retrieval supplied additional historical records; I checked selected original tables locally, not every added scan cell.
- **Independent refitting:** **executed before reading the supplied fitter**. Subsequently executed its fitting function for comparison. I executed **41 fits × two bars**, continuous constrained optimization, analytical lower-bound checks and witness feasibility checks. The packaged reproduction ran successfully and reproduced every floor within **1.13 × 10⁻⁸ wt% Ni**.
- **Full truth:** executed seven-variable floor searches, strictly passing witnesses, reference optimization, a 262,144-design pass-share diagnostic and soft-objective optimization. These full-network minima are best values found, **not global certificates**.
- **CALPHAD:** executed pycalphad spot checks with the hash-matched mc_ni v2.036 database and documented parser adaptations/phase selection. I did not regenerate the full grid or rerun the absent `run_calphad.py` helper. The specific claimed **~50 °C NAB liquidus bias** was inspected as an uploaded caveat, not independently verified experimentally.
- **Policy integration:** inspected the exposed feasibility mask, but could not execute or certify filtering across absent policy/checking scripts.

## Reference and experiment recommendation

**Use dense C70600 as the primary bar if that is the proposal’s promised comparator; treat C71500 as a separate stricter scenario.** Specify cumulative mass loss, maximum local attack, environment, product condition and a prespecified noninferiority margin.

The cheapest direct challenge to **Ni ≥ 10 as necessary** is one plausible sub-10Ni alloy—such as **Cu balance–2Ni–2.1Al–3.6Fe**—and C70600 in the same 30-day test, starting with three independently prepared coupons per material. A convincing pass falsifies that exclusion rule. It does not locate a universal floor.

For model discrimination, I recommend **Ni 0/2/5/10 × Al 0/2.5**, with Fe/Mn fixed, plus pure Cu and the 70–30 reference: **ten materials, 30 coupons at triplicate**, with cleaning controls, measured density/phases and local-attack measurements. Replicate count must ultimately be powered from observed variability.

### Discretionary analytical decisions

- I kept source corrections and endpoint substitutions as separate sensitivities rather than silently replacing the uploaded data.
- I used continuous optimization and analytical certificates where possible, distinguishing those results from local full-network searches and sampled pass shares.
- I capped historical-report influence and separated deployment, participant, duration and endpoint groups to avoid pseudoreplication.
- I treated protective signs, Ni saturation scale, regularization and CALPHAD phase selection as explicit assumptions—not measured facts.
- I retained the unrestricted composition space and recommended testing competing truths before using any corrosion-derived nickel exclusion.