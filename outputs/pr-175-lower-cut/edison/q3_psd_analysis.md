# Edison job-futurehouse-data-analysis-crow-high result: q3_psd_analysis

**Task ID:** `60967197-7577-4f98-bfbd-2fd030b595a4`  
**Status:** success

<details><summary>Query</summary>

```text
The attached files are an SEM image-analysis particle size distribution of an ultrasonically atomized
nickel-aluminium bronze from our AMAZEMET rePOWDER; `context.md` explains every column and the measurement
limits. We want to know what this says about the fine end for our aluminium powder from the same atomizer,
which we plan to sieve with 8 in sieves at 250, 63 and 45 um for laser powder bed fusion.

Please analyse the data in Python and report, with code and figures:

1. Using only counted particles (`included == True`) and the Miles-Lantuejoul `weight`, the cumulative number
   (Q0) and volume (Q3, equivalent spheres) distributions of `ecd_um`, and the fractions below 10, 15, 20, 25,
   32, 45 and 63 um by number and by volume, with 95 % bootstrap intervals resampled over particles and,
   separately, over fields (the powder segregated by size across the stub, so the field interval matters).
2. The detection limit: particles under 10 px (6.7-10 um) are not counted. Bound how much the true
   sub-10 um and sub-15 um fractions could be underestimated, e.g. by fitting a log-normal or Rosin-Rammler to
   the counted data above 15 um and extrapolating, and compare with the counted values.
3. The fraction within the windows 20-63, 15-45, 20-45 and 0-63 um, by volume (that is, by mass), and what a
   lower cut at 20 um or at 15 um would remove from the material that passes a 63 um sieve and from the
   material that passes a 45 um sieve: grams per 100 g of sieved powder, with intervals.
4. Scaling to aluminium. Ultrasonic atomization theory (Lang 1962) gives a median droplet diameter
   d = 0.34 (8 pi sigma / (rho f^2))^(1/3). Using the liquid properties in `context.md`, estimate the size
   ratio of Al-12Si to NAB droplets at the same frequency, and rescale the NAB distribution by that ratio as
   one estimate of the Al distribution. Report the same fractions (below 15, 20, 25 um; within 20-63 and
   15-45 um) for the rescaled distribution. State plainly how uncertain this transfer is (alloy, melt flow
   rate, plate, amplitude, and the fact that the NAB stub may not be representative).
5. Plots: cumulative Q0 and Q3 with the 15, 20, 45 and 63 um lines marked, for NAB and for the rescaled Al
   estimate; and a histogram of the fine end (below 30 um) by number.

End with a short conclusion: given these numbers, does a lower cut at 15-20 um matter for mass yield, and how
many particles in a typical LPBF layer would be below 20 um?

```

</details>

## Main finding

**For the counted particles, a 15–20 µm lower cut costs little mass. The upper cut matters much more for yield.** However, this SEM dataset cannot rule out an unseen ultrafine population, and transferring its distribution to aluminium is only a provisional estimate.

I analysed **5,937 included particles across nine SEM fields**, applying the supplied Miles–Lantuejoul weights. I ran **20,000 particle-bootstrap and 20,000 whole-field-bootstrap replicates**, separately.

### Deliverables

- [Complete reproducibility bundle](data_entry:sem-powder-size-analysis-complete-reproducibili-n9gu): original inputs, **executed notebook**, Python code, numerical tables, figures, assumptions and bibliography.
- [Full report](data_entry:sem-fine-end-analysis-report-kow7)
- [All numerical results and intervals—CSV](data_entry:sem-psd-fractions-and-95-bootstrap-intervals-lyb3)
- [Standalone Python code](data_entry:reproducible-sem-psd-python-code-ea4f)

## 1. Counted NAB distributions

I calculated
\[
Q_0(t)=\frac{\sum_i w_i\mathbf1(d_i<t)}{\sum_iw_i},\qquad
Q_3(t)=\frac{\sum_iw_id_i^3\mathbf1(d_i<t)}{\sum_iw_id_i^3}.
\]
Q3 represents equivalent-sphere volume and, assuming constant density within the alloy, mass. **All entries below are percentages.** The intervals describe resampling uncertainty in the **counted** population—not missed particles or lot representativeness.

### By number, Q0

| Size | Estimate (%) | 95% particle interval | 95% field interval |
|---|---:|---:|---:|
| <10 µm | 0.911 | 0.625–1.230 | 0.450–1.461 |
| <15 µm | 1.593 | 1.238–1.963 | 1.048–2.395 |
| <20 µm | 2.064 | 1.668–2.475 | 1.426–2.984 |
| <25 µm | 2.912 | 2.453–3.387 | 2.198–3.923 |
| <32 µm | 6.187 | 5.563–6.827 | 5.531–6.970 |
| <45 µm | 41.842 | 40.579–43.093 | 37.251–45.609 |
| <63 µm | 84.646 | 83.706–85.571 | 76.401–88.930 |

### By volume/mass, Q3

| Size | Estimate (%) | 95% particle interval | 95% field interval |
|---|---:|---:|---:|
| <10 µm | 0.002033 | 0.001369–0.002813 | 0.000689–0.004704 |
| <15 µm | 0.006791 | 0.005079–0.008725 | 0.004306–0.012266 |
| <20 µm | 0.016468 | 0.012402–0.021239 | 0.010940–0.026762 |
| <25 µm | 0.053194 | 0.041798–0.066466 | 0.033918–0.084316 |
| <32 µm | 0.370852 | 0.314247–0.435892 | 0.179778–0.681591 |
| <45 µm | 8.7871 | 7.8622–9.8383 | 3.9213–16.3103 |
| <63 µm | 30.4751 | 27.3557–33.9449 | 13.9881–53.7317 |

Number D10/D50/D90 are **34.82/46.90/71.46 µm**; volume D10/D50/D90 are **45.78/103.68/208.60 µm**, reproducing the supplied summary to practical precision.

**The field interval matters:** the coarsest field contributes **39.6% of the volume proxy**. Only 1.53% of its volume is <63 µm, versus 35.3–62.4% in the other fields. Nine fields still provide limited information about spatial heterogeneity; field bootstrapping does not make the stub representative of the lot.

![Cumulative number and volume distributions, with field-bootstrap intervals and 15, 20, 45 and 63 µm cuts](data_entry:nab-and-al-estimate-cumulative-fine-end-distrib-8fq8)

The bundle also contains full-range Q0/Q3 plots with **both** particle and field intervals, plus numerical empirical curves. Plot bands are pointwise, not simultaneous confidence bands.

## 2. Detection limit: the correction is not identifiable

The nominal exclusion limits vary from **6.74 to 10.13 µm**. The 35 counted particles below 10 µm therefore do not constitute a complete sub-10 µm sample.

I fitted **left-truncated, weighted number distributions to particles ≥15 µm**, then obtained volume predictions by integrating the third moment. Ordinary untruncated fitting would incorrectly treat the missing lower tail as observed absence.

| Population or extrapolation | <10 µm number | <15 µm number | <10 µm volume | <15 µm volume |
|---|---:|---:|---:|---:|
| Counted | 0.911% | 1.593% | 0.002033% | 0.006791% |
| Whole fitted log-normal | 0.000073% | 0.01644% | 0.000000313% | 0.000228% |
| Whole fitted Weibull/Rosin–Rammler | 2.972% | 6.655% | 0.005245% | 0.03930% |
| Counted + log-normal missing-tail completion | 0.911% | 1.593% | 0.002033% | 0.006791% |
| Counted + Weibull missing-tail completion | 2.626% | 3.301% | 0.003349% | 0.008123% |

For the **completion** scenarios, I retained every counted particle, anchored each field’s population to its weighted count ≥15 µm, and added the model-predicted missing population below that field’s nominal detection limit. This differs from replacing the entire empirical distribution with a fitted family.

**Neither family is a reliable bound.** In the approximately observable 10–15 µm interval, the observed weighted count is **43.29**, versus predictions of **1.02** from the log-normal and **246.18** from the Weibull. The log-normal’s whole-model extrapolation predicts fewer fines than are already counted; the Weibull overpredicts that interval.

Thus, the Weibull completion illustrates underestimation of about **1.7 percentage points by number**, but it is **not an upper confidence limit**. Without assumptions about unseen particles, the true sub-10 and sub-15 fractions can approach 100%. As a counterexample—not a prediction—an unseen 5 µm population comprising only **0.1% of true mass** would raise the sub-10 number fraction to **69.0%**. Higher-magnification measurements are needed to constrain this.

## 3. Sieve windows and lower-cut mass losses

### Mass fraction of the original measured powder

| Window | Mass fraction (%) | 95% particle interval | 95% field interval |
|---|---:|---:|---:|
| 20–63 µm | 30.4586 | 27.3406–33.9288 | 13.9768–53.7050 |
| 15–45 µm | 8.7803 | 7.8556–9.8308 | 3.9161–16.3026 |
| 20–45 µm | 8.7706 | 7.8476–9.8196 | 3.9092–16.2860 |
| 0–63 µm | 30.4751 | 27.3557–33.9449 | 13.9881–53.7317 |

### Grams removed per 100 g already passing the upper sieve

I calculated these conditional losses in each bootstrap replicate as \(100Q_3(l)/Q_3(u)\), rather than dividing interval endpoints.

| Lower cut and upper sieve | Removed, g/100 g | 95% particle interval | 95% field interval |
|---|---:|---:|---:|
| Remove <20 from <63 µm | 0.05404 | 0.04142–0.06797 | 0.03544–0.08662 |
| Remove <15 from <63 µm | 0.02228 | 0.01694–0.02796 | 0.01252–0.03849 |
| Remove <20 from <45 µm | 0.18741 | 0.14332–0.23585 | 0.12242–0.30727 |
| Remove <15 from <45 µm | 0.07728 | 0.05862–0.09700 | 0.04249–0.13831 |

For example, removing <20 µm leaves **99.946 g of each 100 g of <63 µm NAB powder**, or **99.813 g of each 100 g of <45 µm powder**.

Your **250/63/45 µm sieves cannot impose a 15 or 20 µm lower cut**: they can produce 0–63 or 0–45 µm fractions. The 250 µm sieve is a coarse protection step, not a fines-removal step. The 8-inch diameter affects handling and throughput, not the ideal aperture-based fractions. Actual recovery can differ because ECD is not a sieve-passage diameter and real sieving involves agglomeration, blinding and handling losses.

## 4. Aluminium scaling estimate

Using Lang’s number-median droplet scaling ([1962, DOI: 10.1121/1.1909020](https://doi.org/10.1121/1.1909020)), the same-frequency ratio is
\[
r=\left[\frac{\sigma_{Al}/\rho_{Al}}{\sigma_{NAB}/\rho_{NAB}}\right]^{1/3}
=\left[\frac{0.85/2400}{1.25/7000}\right]^{1/3}
=1.2564.
\]

**The Al-12Si estimate is larger, not smaller.** The supplied liquid-property ranges give **1.215–1.298**, a sensitivity range—not a 95% interval. I multiplied every NAB diameter by 1.2564 and kept its number weight. Transferring the entire distribution shape using a median scaling law is an additional assumption.

### Rescaled Al-12Si fractions

All entries are percentages; bootstrap intervals hold the scale ratio fixed.

| Size | Weighting | Estimate (%) | 95% particle interval | 95% field interval |
|---|---|---:|---:|---:|
| <15 µm | Number | 1.2058 | 0.8867–1.5503 | 0.8083–1.7600 |
| <15 µm | Volume/mass | 0.003441 | 0.002488–0.004531 | 0.001741–0.006635 |
| <20 µm | Number | 1.6421 | 1.2830–2.0174 | 1.0808–2.4458 |
| <20 µm | Volume/mass | 0.007428 | 0.005571–0.009534 | 0.004800–0.012997 |
| <25 µm | Number | 2.0639 | 1.6675–2.4754 | 1.4263–2.9835 |
| <25 µm | Volume/mass | 0.016468 | 0.012402–0.021239 | 0.010940–0.026762 |
| 20–63 µm | Number | 60.7966 | 59.5409–62.0374 | 53.8656–65.1932 |
| 20–63 µm | Volume/mass | 16.8130 | 15.0604–18.7787 | 7.5605–30.3738 |
| 15–45 µm | Number | 10.5570 | 9.7817–11.3440 | 9.4986–11.6184 |
| 15–45 µm | Volume/mass | 1.1800 | 1.0300–1.3499 | 0.5291–2.2270 |

At the central scale, the lower cuts remove:

| Upper sieve | Remove <15 µm, g/100 g | Remove <20 µm, g/100 g |
|---|---:|---:|
| 63 µm | 0.0205 | 0.0442 |
| 45 µm | 0.2908 | 0.6277 |

Both bootstrap intervals for these conditional Al losses are in the report and CSV. For example, removing <20 µm from <45 µm gives **0.628 g/100 g**, particle interval **0.474–0.797**, field interval **0.345–1.138**.

Varying **only** the liquid properties changes the estimated 20–63 µm mass yield to **14.38–19.38%** and 15–45 µm yield to **0.835–1.623%**. These sensitivities are separate from the bootstrap intervals.

**This is not a validated aluminium PSD.** Alloy, melt flow rate, wetting and film formation, plate condition/geometry, amplitude and actual vibration coupling can change both the median and distribution shape. The NAB stub may not represent its own lot. Droplet-to-solid dimensional changes are also omitted. The supplied properties support an **Al-12Si scenario**, not a separate quantitative prediction for **6063**. Matching nominal atomizer settings does not remove these uncertainties.

## 5. Fine-end histogram and particles in a layer

![Weighted fine-end number histogram below 30 µm](data_entry:fine-end-weighted-number-histogram-naa0)

The histogram uses **percent of all counted particles per 1 µm bin**. Gray shading marks absent/partial detection; in the Al panel this is the inherited NAB measurement limitation after rescaling.

If recoating preserves the sieved feed’s number distribution:

| Feed, before lower cutting | <20 µm particles per 1,000 | 95% field interval per 1,000 |
|---|---:|---:|
| NAB, <63 µm | 24.4 | 16.3–37.6 |
| NAB, <45 µm | 49.3 | 33.1–76.6 |
| Scaled Al, <63 µm | 26.3 | 16.9–41.4 |
| Scaled Al, <45 µm | 139.6 | 92.3–210.9 |

An absolute count for a “typical” layer needs its **area, thickness and packing fraction**. For illustration only, a **1 cm², 30 µm layer at 50% solid packing** gives about **514 sub-20 µm particles** with scaled-Al <63 µm feed, or **7,306** with <45 µm feed. These assume the feed PSD carries into the layer without segregation and exclude unseen fines; they are not measured Aconity layer counts.

### Analytical decisions

- I retained all included particles, including flagged regions, and used corrected ECD with equivalent-sphere volumes.
- I estimated the weighted pooled population, resampling particles uniformly or nine whole fields uniformly while retaining their correction weights; I did not convert the target into an equal-field average.
- I kept resampling intervals, detection-limit scenarios and material-transfer uncertainty separate.
- I treated sieve cuts as ideal ECD thresholds and used midpoint liquid properties for the central Al-12Si scenario.
- I reported layer counts per 1,000 first; the absolute layer example is explicitly hypothetical.

### Short conclusion

**On the counted data, a 15–20 µm lower cut barely affects mass yield; the 45 versus 63 µm upper cut dominates.** Nevertheless, fines can be numerous: approximately **24–49 particles per 1,000** in sieved NAB, or **26–140 per 1,000** in the scaled-Al scenario, are below 20 µm before lower cutting. I would verify representative aluminium lots at higher magnification before using these estimates to waive a lower cut or specify LPBF feedstock.
