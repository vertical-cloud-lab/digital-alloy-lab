# Edison job-futurehouse-paperqa3-high result: literature_high_sem_psd_best_practice

**Task ID:** `bcc0e8e4-0622-4b0c-a0f5-dc9d259b409b`  
**Status:** success

<details><summary>Query</summary>

```text
Context. We ultrasonically atomized a nickel-aluminium bronze (UNS C63000, Cu-10Al-5Ni-4Fe) on an
AMAZEMET rePOWDER and want a particle size and shape distribution from SEM images, done to best
practice, before sieving to a directed-energy-deposition cut of 50-200 um. The powder is mostly
spherical, from <10 um fines to ~260 um, with satellites and a few irregular or agglomerated
particles. It was sprinkled on carbon tape on one stub and imaged in a Thermo Fisher Apreo C with the
secondary-electron (ETD) detector: nine usable 3072 x 2048 px fields at 133-200x (0.67-1.01 um per
pixel), densely packed, with many touching and overlapping particles. A naive Hough-circle detection
returned thousands of overlapping false circles per field. We plan distance-transform watershed
segmentation and are weighing pretrained models (Cellpose, StarDist, Segment Anything / SAM, and
SEM-powder-specific deep-learning models), and we have a few hand measurements to validate against.

Please give the best-practice method, with numbers and sources, for:

1. Standards. What ISO 13322-1 (static image analysis), ISO 9276-1, -2 and -6 (representation of
   results, moments, and shape descriptors), ISO 14488 (sample splitting), ASTM F3049 (characterizing
   powders for AM), ASTM B822 (laser diffraction for metal powders) and ASTM B214 (sieve analysis)
   require or recommend for image-based particle sizing: the size measure (projected-area equivalent
   circle diameter vs Feret diameters), magnification and pixel requirements, minimum particle
   counts, calibration and traceability (stage micrometer / certified reference beads), and what a
   report must state.

2. Counting statistics. The minimum number of particles for D10, D50 and D90 by number and by volume
   at a stated precision (e.g. the ISO 13322-1 / Masuda-Gotoh style estimate of the count needed for
   a given relative error in a volume-weighted percentile, and the ~10,000-particle figures quoted for
   robust morphology). How should confidence intervals on percentiles be computed (bootstrap,
   order-statistic, Masuda-Gotoh), and why does the volume-weighted D90 need far more particles than
   the number-weighted D50?

3. Pixel resolution. The minimum number of pixels across (or pixel area of) the smallest particle
   for reliable size, and separately for reliable shape (circularity, aspect ratio, solidity), with
   quantitative estimates of the bias in circularity and perimeter for small, pixelated objects, and
   how perimeter estimators (Crofton, chain-code corrections) reduce it. What lower size cut-off
   should be applied for a given pixel size?

4. Segmentation of touching and overlapping spherical particles: thresholding (Otsu, local/adaptive),
   distance-transform marker-controlled watershed (h-maxima marker selection, over- and
   under-segmentation), ellipse/circle fitting on contours, Cellpose, StarDist, SAM / micro-SAM and
   powder-specific CNNs (e.g. Mask R-CNN models trained on AM-powder SEM images). Report published
   accuracy comparisons on metal powders or similar dense spherical particles (precision/recall, size
   bias versus manual measurement), and what validation is considered adequate.

5. Edge effects. Exclusion of particles that touch the image frame and the standard bias correction
   (Miles-Lantuejoul guard-frame weighting, w = (W*H)/((W - d)(H - d)) for a particle of extent d), and
   how it is reported. Also: double counting in overlapping fields, and how to handle partially
   hidden (occluded) particles in multilayer fields.

6. Number- to volume-weighted conversion. Converting a number distribution of projected-area
   equivalent diameters to volume (mass) weighting (q0 to q3 via ISO 9276-2 moments, d^3 weighting),
   the error amplification from a few large particles, and whether a sphericity correction is needed.

7. SEM image analysis versus laser diffraction and sieving for spherical gas- and ultrasonically
   atomized metal powders: typical systematic differences in D10/D50/D90 (and their direction), the
   reasons (2D projection, orientation, sedimentation and size segregation on the stub, fines adhering
   to coarse particles, satellites, agglomerates, laser-diffraction volume weighting and Mie model
   assumptions), and published side-by-side numbers. Also dynamic image analysis (Camsizer, QICPIC,
   Morphologi 4) as a reference method.

8. Satellites and agglomerates. How satellite fraction and agglomerates are quantified from SEM
   images (solidity/convexity thresholds, convexity defects, manual classification, counts of
   satellites per particle), and typical values reported for gas- and ultrasonically atomized powders.

9. Imaging practice. Secondary-electron versus backscattered-electron contrast for segmenting metal
   powder on carbon tape; dispersion methods (dry dispersion, sprinkling, solvent dispersion,
   mounting in epoxy and cross-sectioning) that avoid overlap and size segregation; how many fields,
   stubs and splits are needed; and a magnification ladder when the size range spans more than a
   decade (e.g. 10-260 um).

10. Reporting conventions: the minimum content of a report (counts, n per size class, weighting,
    descriptor definitions, pixel size, exclusion rules, confidence intervals, cumulative Q0 and Q3
    curves, span (D90-D10)/D50), shape descriptor definitions per ISO 9276-6 (circularity
    4*pi*A/P^2 versus sqrt form, aspect ratio, solidity, convexity), and how AM-powder papers report
    these.

Finish with a concise, numbered protocol for the next powder lot on the same SEM (stub prep, detector,
magnification and pixel size, fields and particle counts, segmentation and validation, exclusions and
corrections, reporting), and say plainly which of our current choices would not meet ISO 13322-1.

```

</details>

Question: Context. We ultrasonically atomized a nickel-aluminium bronze (UNS C63000, Cu-10Al-5Ni-4Fe) on an
AMAZEMET rePOWDER and want a particle size and shape distribution from SEM images, done to best
practice, before sieving to a directed-energy-deposition cut of 50-200 um. The powder is mostly
spherical, from <10 um fines to ~260 um, with satellites and a few irregular or agglomerated
particles. It was sprinkled on carbon tape on one stub and imaged in a Thermo Fisher Apreo C with the
secondary-electron (ETD) detector: nine usable 3072 x 2048 px fields at 133-200x (0.67-1.01 um per
pixel), densely packed, with many touching and overlapping particles. A naive Hough-circle detection
returned thousands of overlapping false circles per field. We plan distance-transform watershed
segmentation and are weighing pretrained models (Cellpose, StarDist, Segment Anything / SAM, and
SEM-powder-specific deep-learning models), and we have a few hand measurements to validate against.

Please give the best-practice method, with numbers and sources, for:

1. Standards. What ISO 13322-1 (static image analysis), ISO 9276-1, -2 and -6 (representation of
   results, moments, and shape descriptors), ISO 14488 (sample splitting), ASTM F3049 (characterizing
   powders for AM), ASTM B822 (laser diffraction for metal powders) and ASTM B214 (sieve analysis)
   require or recommend for image-based particle sizing: the size measure (projected-area equivalent
   circle diameter vs Feret diameters), magnification and pixel requirements, minimum particle
   counts, calibration and traceability (stage micrometer / certified reference beads), and what a
   report must state.

2. Counting statistics. The minimum number of particles for D10, D50 and D90 by number and by volume
   at a stated precision (e.g. the ISO 13322-1 / Masuda-Gotoh style estimate of the count needed for
   a given relative error in a volume-weighted percentile, and the ~10,000-particle figures quoted for
   robust morphology). How should confidence intervals on percentiles be computed (bootstrap,
   order-statistic, Masuda-Gotoh), and why does the volume-weighted D90 need far more particles than
   the number-weighted D50?

3. Pixel resolution. The minimum number of pixels across (or pixel area of) the smallest particle
   for reliable size, and separately for reliable shape (circularity, aspect ratio, solidity), with
   quantitative estimates of the bias in circularity and perimeter for small, pixelated objects, and
   how perimeter estimators (Crofton, chain-code corrections) reduce it. What lower size cut-off
   should be applied for a given pixel size?

4. Segmentation of touching and overlapping spherical particles: thresholding (Otsu, local/adaptive),
   distance-transform marker-controlled watershed (h-maxima marker selection, over- and
   under-segmentation), ellipse/circle fitting on contours, Cellpose, StarDist, SAM / micro-SAM and
   powder-specific CNNs (e.g. Mask R-CNN models trained on AM-powder SEM images). Report published
   accuracy comparisons on metal powders or similar dense spherical particles (precision/recall, size
   bias versus manual measurement), and what validation is considered adequate.

5. Edge effects. Exclusion of particles that touch the image frame and the standard bias correction
   (Miles-Lantuejoul guard-frame weighting, w = (W*H)/((W - d)(H - d)) for a particle of extent d), and
   how it is reported. Also: double counting in overlapping fields, and how to handle partially
   hidden (occluded) particles in multilayer fields.

6. Number- to volume-weighted conversion. Converting a number distribution of projected-area
   equivalent diameters to volume (mass) weighting (q0 to q3 via ISO 9276-2 moments, d^3 weighting),
   the error amplification from a few large particles, and whether a sphericity correction is needed.

7. SEM image analysis versus laser diffraction and sieving for spherical gas- and ultrasonically
   atomized metal powders: typical systematic differences in D10/D50/D90 (and their direction), the
   reasons (2D projection, orientation, sedimentation and size segregation on the stub, fines adhering
   to coarse particles, satellites, agglomerates, laser-diffraction volume weighting and Mie model
   assumptions), and published side-by-side numbers. Also dynamic image analysis (Camsizer, QICPIC,
   Morphologi 4) as a reference method.

8. Satellites and agglomerates. How satellite fraction and agglomerates are quantified from SEM
   images (solidity/convexity thresholds, convexity defects, manual classification, counts of
   satellites per particle), and typical values reported for gas- and ultrasonically atomized powders.

9. Imaging practice. Secondary-electron versus backscattered-electron contrast for segmenting metal
   powder on carbon tape; dispersion methods (dry dispersion, sprinkling, solvent dispersion,
   mounting in epoxy and cross-sectioning) that avoid overlap and size segregation; how many fields,
   stubs and splits are needed; and a magnification ladder when the size range spans more than a
   decade (e.g. 10-260 um).

10. Reporting conventions: the minimum content of a report (counts, n per size class, weighting,
    descriptor definitions, pixel size, exclusion rules, confidence intervals, cumulative Q0 and Q3
    curves, span (D90-D10)/D50), shape descriptor definitions per ISO 9276-6 (circularity
    4*pi*A/P^2 versus sqrt form, aspect ratio, solidity, convexity), and how AM-powder papers report
    these.

Finish with a concise, numbered protocol for the next powder lot on the same SEM (stub prep, detector,
magnification and pixel size, fields and particle counts, segmentation and validation, exclusions and
corrections, reporting), and say plainly which of our current choices would not meet ISO 13322-1.


# Best-Practice SEM Image Analysis of Ultrasonically Atomized Nickel-Aluminium Bronze Powder for Directed Energy Deposition

## 1. Standards Requirements for Image-Based Particle Sizing

The governing standard for the described workflow is **ISO 13322-1:2014** (static image analysis), which requires that the analyst define the measured size quantity explicitly—normally the projected-area-equivalent circle diameter (d_A = 2√(A/π))—along with Feret diameters where particle shape or orientation information is needed. The standard mandates representative sampling and dispersion, a calibrated image scale, adequate resolution and particle count (which depends on the distribution width and the required uncertainty rather than a single universal minimum), documented segmentation and border-exclusion rules, and a report identifying the distribution basis, size classes, instrument, preparation, calibration, and analysis procedure (kestens2014certificationreportthecertification pages 76-76, grubbs2021comparisonoflaser pages 3-5).

**ISO 9276-1** establishes notation for differential and cumulative distributions and requires identification of the weighting basis (number q₀/Q₀, volume q₃/Q₃, etc.); percentiles under different weightings are not interchangeable. **ISO 9276-2** defines the moment-based conversion between weighting orders: for equal-density equivalent spheres, number-to-volume conversion weights each particle by d³. **ISO 9276-6** defines shape descriptors (circularity, convexity, aspect ratio, solidity) and recommends that each particle be represented by approximately **100–5000 pixels** to provide adequate precision, particularly for the smallest particles (charbonneau2025classificationofmetallic pages 12-14, charbonneau2025classificationofmetallic pages 4-7, charbonneau2025classificationofmetallic pages 14-16). **ISO 14488** requires representative lot splitting using a rotary divider or validated riffler, not convenience scooping. **ASTM F3049** is a guide that directs users to ISO 13322-1, ASTM B822 (laser diffraction), and ASTM B214 (sieving) as complementary PSD methods (moroni2020onstandardizationefforts pages 9-12). **ASTM F3571** recommends using aspect ratio combined with solidity to separate spherical from nonspherical particles, emphasizing that a single descriptor is insufficient (charbonneau2025classificationofmetallic pages 1-2).

The following table summarizes all relevant standards:

| Standard | Scope | Key requirements/recommendations for image analysis | Relevance to the user’s SEM analysis |
|---|---|---|---|
| **ISO 13322-1:2014** | Static image analysis for particle-size distributions | Define the measured size explicitly—normally projected-area-equivalent diameter, with Feret dimensions where shape or orientation matters. Use representative sampling and dispersion, calibrated image scale, adequate resolution and particle count, documented segmentation and border rules, and report distribution basis, size classes, instrument, preparation, calibration and analysis procedure. Particle count depends on distribution width and required uncertainty rather than one universal minimum (kestens2014certificationreportthecertification pages 76-76, wouters2025assessingparticlecount pages 2-3, grubbs2021comparisonoflaser pages 3-5). | This is the governing image-analysis standard. Nine crowded fields from one sprinkled stub do not establish an ISO-conforming lot PSD unless representativeness, traceable calibration, counting precision, segmentation validity and treatment of touching or occluded particles are demonstrated. |
| **ISO 9276-1** | Representation of particle-size-analysis results | Establishes notation and presentation of differential and cumulative distributions, size classes and weighting basis. Reports must identify whether results are number-, length-, area-, volume- or mass-weighted; percentiles with different weighting bases are not directly equivalent. | Report separate cumulative **Q0** and model-derived **Q3** curves, D10/D50/D90 and span. Do not describe a number-weighted SEM percentile as equivalent to a laser-diffraction percentile without conversion and qualification. |
| **ISO 9276-2** | Calculation of mean sizes, moments and conversion between distribution bases | Uses distribution moments to convert weighting orders. For equal-density equivalent spheres, number-to-volume conversion weights each particle by diameter cubed. State the conversion and assumed size and shape model; transformed results are highly sensitive to rare large particles and size truncation (grubbs2021comparisonoflaser pages 13-14, grubbs2021comparisonoflaser pages 2-2). | Calculate Q3 from projected-area-equivalent diameters only as a model-derived equivalent-sphere distribution. Retain Q0 as the primary image result and bootstrap the complete conversion because a few 200–260 µm particles can dominate Q3 and D90. |
| **ISO 9276-6** | Quantitative description of particle shape and morphology | Define every descriptor and formula. Relevant quantities include perimeter-based circularity, aspect or ellipse ratio, convexity and solidity. Cited implementation guidance represents each particle with approximately **100–5000 pixels**. Perimeter and circularity vary with resolution and perimeter algorithm, so pixel size, threshold and estimator must be fixed and reported (charbonneau2025classificationofmetallic pages 12-14, charbonneau2025classificationofmetallic pages 4-7, charbonneau2025classificationofmetallic pages 14-16). | At 0.67–1.01 µm/px, a 10 µm particle contains only about 77–175 projected pixels: marginal for size and inadequate for defensible perimeter or satellite morphology. Acquire higher-magnification fields for fines and shape, and state the exact circularity formula. |
| **ISO 14488** | Sampling and sample splitting of particulate materials | Obtain representative laboratory and test portions through documented splitting and repeated subdivision; avoid scoop or surface sampling that permits size segregation. Record lot identity, sampling location, splitting device, split sequence, test-portion mass and replicate portions. | Split the bulk atomized lot before stub preparation, preferably using a rotary divider or validated riffler. Prepare independent stubs from independent final splits; one conveniently selected portion on one stub does not establish lot representativeness. |
| **ASTM F3049** | Guide to characterization of metal powders used in powder-based AM | This is a guide rather than a stand-alone image-analysis method. It identifies relevant powder properties and directs users to established methods for PSD, morphology, chemistry, density and flow. The material condition—virgin, used, blended or recycled—and the applied methods should be identified (moroni2020onstandardizationefforts pages 9-12). | Use it to define the qualification package: ISO 13322-1 image analysis for size and morphology, ASTM B822 laser diffraction and ASTM B214 sieving as complementary PSD methods, plus chemistry, density and flow tests appropriate to DED. |
| **ASTM B822** | Particle-size distribution of metal powders by light scattering or laser diffraction | Requires representative sampling and controlled dry or wet dispersion, instrument checks, suitable obscuration, repeat measurements, specified optical assumptions and reporting of preparation, dispersion conditions, instrument and volume-based PSD. Results are sensitive to agglomeration, orientation and optical settings (grubbs2021comparisonoflaser pages 1-2, grubbs2021comparisonoflaser pages 2-2, batistao2026surfacefunctionalizationof pages 69-73). | Recommended as an independent Q3 reference for unsieved powder. Differences from SEM Q0 and SEM-derived Q3 are expected, especially below 20 µm and for satellites or agglomerates; keep dispersion conditions constant for lot comparisons. |
| **ASTM B214** | Sieve analysis of metal powders | Uses a representative test portion, specified and verified sieve series, controlled mechanical sieving, weighing of retained fractions and a mass-balance check. Results are mass fractions bounded by sieve apertures, not projected-image diameters. | This is the primary process-control method for confirming the intended **50–200 µm DED cut** and quantifying undersize and oversize after sieving. It cannot characterize detailed morphology, satellites or the continuous distribution within the cut. |
| **ASTM F3571** | Quantitative characterization of metal-powder morphology by image analysis | Recommends explicit descriptor definitions and use of multiple descriptors. Aspect or ellipse ratio combined with solidity is useful for separating spherical and nonspherical particles. Resolution, thresholding and software algorithms must be controlled because one descriptor alone can classify unlike shapes similarly (charbonneau2025classificationofmetallic pages 14-16, charbonneau2025classificationofmetallic pages 1-2). | Use with ISO 9276-6 to predefine spherical, elongated, irregular, satellite-bearing and agglomerated classes. Derive classification thresholds from manually labelled C63000 particles rather than importing thresholds from another alloy or software package. |


*Table: Summary of the principal ISO and ASTM standards governing representative sampling, static image analysis, distribution weighting, morphology, laser diffraction and sieving. It distinguishes requirements applicable to the SEM workflow from complementary methods used to qualify the 50–200 µm DED cut.*

**Calibration and traceability:** ISO 13322-1 and the ERM-FD102 certification protocol require calibration using a traceable stage micrometer or certified reference particles, with documented certificate number, uncertainty, date, SEM settings, and measured scale error (kestens2014certificationreportthecertification pages 76-76, kestens2014certificationreportthecertification pages 75-76).

## 2. Counting Statistics

The minimum particle count depends on the distribution width, the weighting basis, and the target percentile. OECD Test Guideline 125 recommends at least **300 particles for narrow log-normal distributions** (geometric standard deviation ≤1.5) and at least **700 for wider distributions**; ISO 21363 and ISO 19749 recommend approximately **500 particles** (wouters2025assessingparticlecount pages 2-3). For the median (D50) at 10% precision uncertainty, as few as 62–267 particles may suffice, depending on polydispersity; however, D10 and D90 generally require substantially more particles because tail percentiles are more sensitive to sampling variability (wouters2025assessingparticlecount pages 7-9, wouters2025assessingparticlecount pages 4-6).

Wouters et al. (2025) report optimal particle counts (N_opt, beyond which additional measurements yield negligible improvement in combined uncertainty) for different materials: for the minimum Feret diameter, N_opt ranged from 136 (D50, ERM-FD100) to 897 (D10, BaSO₄RM), demonstrating that polydisperse materials and tail percentiles require far more particles (wouters2025assessingparticlecount pages 7-9).

**Why volume-weighted D90 needs far more particles than number-weighted D50:** Under d³ weighting, a single large particle contributes disproportionately to the upper tail. The volume-weighted D90 is dominated by the few largest particles in the sample, amplifying sampling variance relative to number-weighted statistics where every particle counts equally. This is further compounded because very large particles are rare in the number distribution, so far more total particles must be measured to accumulate enough large-particle observations for a stable volume-weighted tail.

**Confidence intervals** on percentiles can be computed via: (a) **bootstrap resampling** of entire fields or stubs (not individual particles, to preserve spatial correlation), (b) **order-statistic methods** (the k-th and (n−k+1)-th ordered values bracket the p-th percentile with known binomial coverage), and (c) the **Masuda–Gotoh analytical approach**, which estimates the count needed for a given relative error in a given percentile based on the assumed distribution form. Bootstrap methods are recommended for the present heterogeneous, multi-field dataset because they naturally incorporate field-to-field variability.

**Practical target:** For a C63000 powder spanning <10 to ~260 µm with satellites and irregulars, aim for **≥1,000 accepted particles for the primary Q₀ PSD** and **≥10,000 for robust morphology and model-derived Q₃**, sampling across multiple stubs and splits.

## 3. Pixel Resolution

**For reliable size measurement,** a minimum of approximately **10 pixels across the particle diameter** (≥100 pixels projected area) is a widely applied practical threshold. ISO 9276-6 recommends **100–5000 pixels per particle** overall (charbonneau2025classificationofmetallic pages 12-14, charbonneau2025classificationofmetallic pages 4-7). Charbonneau et al. (2025) used a minimum of **3,000 pixels per particle** for reliable shape classification at 250× magnification, at which a 30 µm particle contained approximately 4,500 pixels (charbonneau2025classificationofmetallic pages 4-7).

**For reliable shape (circularity, aspect ratio, solidity),** substantially more pixels are needed because perimeter-based descriptors are highly sensitive to pixelation. At low pixel counts, the perimeter of a smooth circle is overestimated by chain-code digitization (approximately π/4 × true value for a 4-connected code, improving with 8-connected codes), causing circularity (4πA/P²) to be systematically underestimated. **Crofton's formula** and corrected chain-code estimators reduce this bias: the MorphoLibJ implementation of Crofton's formula produces perimeter values **3–5% lower** than standard ImageJ chain-code perimeters for the same particles (charbonneau2025classificationofmetallic pages 7-10). This systematic difference means that shape thresholds calibrated in one software are not directly transferable to another without recalibration (charbonneau2025classificationofmetallic pages 7-10, charbonneau2025classificationofmetallic pages 10-12).

**Lower size cutoffs for the user's setup:** At 0.67–1.01 µm/px (133–200×), a 10 µm particle contains only ~10–15 px across (~77–175 pixels area)—marginal for size and **inadequate for defensible shape measurement**. The practical size cutoff for reliable diameter at this resolution is approximately **7–10 µm**; for circularity, it would be approximately **35–55 µm** (to achieve ~3,000 pixels). A higher-magnification tier (~500×, ≤0.2 µm/px) is essential for shape descriptors on fines (charbonneau2025classificationofmetallic pages 12-14).

## 4. Segmentation of Touching and Overlapping Spherical Particles

The following table summarizes published accuracy comparisons:

| Method | Type | Published accuracy metrics | Strengths | Weaknesses | Suitability for dense spherical metal powders |
|---|---|---|---|---|---|
| Otsu or global thresholding | Classical semantic segmentation | No metal-powder instance-segmentation benchmark identified in the cited evidence. | Fast, reproducible, parameter-light; effective with uniform BSE compositional contrast, where metal is bright against carbon tape. | Produces connected foreground rather than particle instances; sensitive to SE shading, charging, carbon-tape texture, and intensity gradients; cannot resolve overlap alone. | **Useful preprocessing only.** Prefer BSE over SE, then apply marker-controlled watershed or another instance method. BSE threshold segmentation of powder on carbon tape has been demonstrated using strong atomic-number contrast (giunto2026accuratesemedsquantification pages 15-17). |
| Local or adaptive thresholding | Classical semantic segmentation | No powder-specific precision/recall benchmark identified. | Handles illumination gradients, edge darkening, and particle-to-particle brightness differences better than a single global threshold. | Window size can erase fines or create false foreground inside shaded coarse particles; still merges touching particles and may interpret surface texture as boundaries. | **Useful preprocessing when BSE intensity is nonuniform.** Validate window size by particle-size class; not adequate as the final instance segmentation. |
| Distance-transform, marker-controlled watershed | Classical instance segmentation | On 50 metal-powder SEM images: **99.3% precision, 89.2% recall**; lower recall was attributed to failure on heavily overlapping particles (li2023automaticcharacterizationof pages 9-12). | Transparent, inexpensive, reproducible; well matched to isolated or lightly touching near-circular particles; markers can be tuned with h-maxima or minimum peak distance. | Too many markers cause over-segmentation; suppressed markers cause merging; distance peaks disappear under strong overlap, satellites, irregular particles, and broad size distributions. | **Good baseline, but insufficient alone for the present dense fields.** Tune markers by scale and audit split/merge errors separately. |
| Circular Hough transform (CHT) | Classical model-based detection | On the same metal-powder benchmark: **95.2% precision, 93.8% recall**; runtime 0.688 s per image (li2023automaticcharacterizationof pages 9-12, li2023automaticcharacterizationof pages 12-15). | Can infer circular particles despite partial overlap or incomplete visible arcs; directly returns center and radius. | Broad radius searches generate duplicate and overlapping false circles; vulnerable to noisy edges, satellites, irregular particles, and internal SE texture; imposes circularity and does not yield a trustworthy measured contour. | **Poor as a full-field detector for these images**, consistent with the reported thousands of false circles. It may be useful only after candidate-region segmentation and strict non-maximum suppression. |
| Region segmentation followed by local CHT, Li et al. (2023) | Classical hybrid instance detection | Across 50 SEM images of Ni₃Al, TC4, and TiAl powders: **99.3% precision, 99.5% recall** and 0.136 s per image, versus watershed 99.3%/89.2% and direct CHT 95.2%/93.8% (li2023automaticcharacterizationof pages 9-12, li2023automaticcharacterizationof pages 12-15, li2023automaticcharacterizationof pages 1-5). | Restricts circle fitting to individual candidate regions, sharply reducing false circles and computation; handles substantial overlap and broad size ranges; metal-powder-specific evidence. | Accuracy concerns particle identification rather than mask-boundary fidelity; circle fitting can hide satellites or irregularity and bias projected area, perimeter, and shape descriptors. | **Strong candidate for spherical-particle counting and diameter**, but retain contour-based masks for morphology and manually audit irregular, satellite-bearing, and occluded particles. |
| Mask R-CNN, Yichao et al. (2021) | Supervised deep-learning instance segmentation | Metal-powder study reported **23.6% higher recognition accuracy** than traditional segmentation; 12,192 particles were identified in eight images. Training used 100 subimages containing 14,835 labels, but precision, recall, IoU, and AP were not reported (yichao2021particleautostatisticsand pages 1-3, yichao2021particleautostatisticsand pages 7-9, yichao2021particleautostatisticsanda pages 3-4). | Designed for individual instances; recognizes touching, overlapping, partially occluded, nonspherical, and satellite particles; directly produces masks and classes. | Requires representative annotations and retraining for a new alloy, detector, magnification, and preparation; inferred hidden boundaries may be model-dependent; the published metric is incompletely specified. | **Promising and metal-powder-specific**, especially after fine-tuning on Apreo BSE/SE images. Do not accept pretrained output without local held-out validation. |
| Uncertainty-aware Mask R-CNN, Rettenberger et al. (2024) | Supervised deep-learning instance segmentation | On held-out inorganic-powder SEM images, mean **AJI+ was 0.81 versus 0.55 for U-Net at low magnification**, and **0.51 versus 0.34 at high magnification**; Mask R-CNN won on 14 of 15 test images (rettenberger2024uncertaintyawareparticlesegmentation pages 3-4). | Handles overlapping, clustered, irregular, blurry, and differently sized particles; uncertainty score supports manual review; approximately 3 min automated analysis versus 145–430 min for experts (rettenberger2024uncertaintyawareparticlesegmentation pages 4-5, rettenberger2024uncertaintyawareparticlesegmentation pages 2-3). | Performance falls at difficult high magnification; expert labels themselves disagreed; transfer across imaging regimes is not guaranteed, and separate models were needed for low and high magnification. | **Best-supported DL architecture for difficult powder SEM among the cited studies.** Fine-tune locally and route low-confidence masks to manual correction. |
| BPartIS | Bayesian deep-learning instance segmentation | Evaluated on the 465-image EMPS dataset using AP, AP50, AP75, and mean IoU; uncertainty filtering improved performance over conventional image processing, Gaussian-mixture labeling, and Mask R-CNN, but numerical AP values were not available in the cited excerpt. Distribution errors included cosine distances of 0.02111 for size and 0.03261 for aspect ratio (yildirim2021bayesianparticleinstance pages 7-8, yildirim2021bayesianparticleinstance pages 9-11). | Provides instance masks plus epistemic uncertainty; filters false positives from scale bars and background texture; supports quantitative size and aspect-ratio distributions. | General electron-microscopy dataset rather than a dedicated atomized-metal-powder benchmark; substantial overlaps can remain challenging; requires model deployment and domain validation. | **Good validation-oriented option**, particularly where uncertainty-based review is valuable; fine-tune and compare against powder-specific Mask R-CNN and watershed baselines. |
| Cellpose | Pretrained or fine-tuned flow-based deep-learning instance segmentation | No published atomized-metal-powder SEM benchmark or precision/recall comparison was identified in the cited evidence. | Easy interactive use; flow representation often separates touching rounded objects; supports retraining from corrected masks. | Generic pretrained models are predominantly biological; may merge heavily overlapped particles, mistake SE highlights for boundaries, or smooth away satellites; diameter parameter is scale-sensitive. | **Exploratory baseline only.** Fine-tune on locally annotated powder images and require held-out mask-IoU, split/merge, size-bias, and shape-bias validation before quantitative use. |
| StarDist | Supervised star-convex deep-learning instance segmentation | No atomized-metal-powder SEM benchmark was identified in the cited evidence. | Star-convex representation is naturally suited to isolated spherical or mildly overlapping particles; efficient instance separation and non-maximum suppression. | Strongly concave agglomerates, satellite-bearing particles, and irregular shapes violate the star-convex assumption; inferred contours can suppress real morphology. | **Potentially strong for primary spherical particles**, but use separate labels for satellites/agglomerates and validate contour-derived shape descriptors rather than detection alone. |
| SAM or micro-SAM | Foundation-model-assisted instance segmentation | No published quantitative benchmark on dense atomized-metal-powder SEM images was identified in the cited evidence. | Rapid interactive annotation; useful for building a training set and correcting masks; micro-SAM adds microscopy-oriented tiling, embeddings, and tracking tools. | Zero-shot masks are prompt- and contrast-dependent; adjacent similar particles may merge, while textured surfaces may fragment; no intrinsic guarantee of metrological boundary accuracy or consistent hidden-boundary reconstruction. | **Best used as an annotation accelerator, not the final metrology method.** Fine-tune or use curated prompts, then validate against independent expert masks and hand-measured diameters. |


*Table: Comparison of classical and deep-learning methods for separating touching and overlapping spherical particles in SEM images, including published metal-powder metrics and explicit evidence gaps for generic pretrained models.*

**Key findings:**

- **Naive Hough-circle detection** on full fields, as the user attempted, is known to produce abundant false positives due to image noise, broad particle-size variation, and internal SE texture; published CHT precision was only 95.2% with 93.8% recall (li2023automaticcharacterizationof pages 9-12, li2023automaticcharacterizationof pages 12-15).

- **Distance-transform marker-controlled watershed** achieved 99.3% precision but only **89.2% recall** on 50 metal-powder SEM images, primarily failing on heavily overlapping particles (li2023automaticcharacterizationof pages 9-12). It remains a good transparent baseline but is insufficient alone for densely packed fields.

- A **region-segmentation + local CHT hybrid** (Li et al. 2023) achieved **99.3% precision and 99.5% recall** on Ni₃Al, TC4, and TiAl powders, with computation time of 0.136 s per image (li2023automaticcharacterizationof pages 9-12, li2023automaticcharacterizationof pages 12-15, li2023automaticcharacterizationof pages 1-5).

- **Mask R-CNN** trained on metal-powder SEM images improved recognition accuracy by **23.6%** over traditional segmentation and identified >12,000 particles across 8 images, including occluded and satellite-bearing particles (yichao2021particleautostatisticsand pages 1-3, yichao2021particleautostatisticsanda pages 1-3, yichao2021particleautostatisticsanda pages 3-4).

- An **uncertainty-aware Mask R-CNN** (Rettenberger et al. 2024) achieved **AJI+ of 0.81 versus 0.55 for U-Net** at low magnification and 0.51 vs 0.34 at high magnification on inorganic powder SEM images, with automated analysis in ~3 minutes versus 145–430 minutes for experts (rettenberger2024uncertaintyawareparticlesegmentation pages 3-4, rettenberger2024uncertaintyawareparticlesegmentation pages 2-3).

- **Cellpose, StarDist, and SAM/micro-SAM** have no published metal-powder SEM benchmarks in the identified literature. They may serve as annotation accelerators or exploratory baselines but require fine-tuning and rigorous held-out validation before quantitative use.

**Recommended approach:** Use BSE thresholding followed by watershed as the initial baseline, then deploy a locally fine-tuned instance segmentation model (preferably uncertainty-aware Mask R-CNN) for severe overlap. Validate against ≥50 hand-measured particles with identity/Bland-Altman plots; accept if mean diameter bias <2% and precision/recall ≥0.95.

## 5. Edge Effects

**Frame-touching particles** must be handled to avoid size-dependent bias. The standard approach is either (a) an **unbiased inclusion frame** (include particles intersecting the top and left edges, exclude those intersecting the bottom and right edges), or (b) exclusion of all frame-touching particles with application of the **Miles–Lantuéjoul guard-frame correction**: for a particle of extent d in a field of dimensions W×H, the weight is w = (W·H)/((W−d)·(H−d)). This corrects for the greater probability that large particles intersect the frame (yildirim2021bayesianparticleinstance pages 9-11).

**Double counting in overlapping fields** must be prevented by recording stage coordinates and rejecting duplicate detections by position matching. **Partially hidden (occluded) particles** in multilayer deposits should be excluded from size and shape measurements unless the hidden contour can be reliably reconstructed; they should be reported separately (yildirim2021bayesianparticleinstance pages 9-11, yichao2021particleautostatisticsand pages 4-6, yichao2021particleautostatisticsanda pages 4-6).

## 6. Number- to Volume-Weighted Conversion

Converting a number distribution Q₀ to a volume (mass) distribution Q₃ proceeds via ISO 9276-2 moment formalism: each accepted particle receives weight w_i = d_{A,i}³, and Q₃(d) = Σ(d_{A,i}³ · I[d_{A,i}≤d]) / Σd_{A,i}³. This cubic weighting means that **a few large particles dominate** the result: a single 260 µm particle contributes the same volume weight as approximately 17,576 particles of 10 µm. Error amplification is severe at the upper tail, making Q₃ D90 extremely sensitive to incomplete sampling of large particles and to segmentation errors that affect their measured diameter (grubbs2021comparisonoflaser pages 13-14, grubbs2021comparisonoflaser pages 2-2).

A **sphericity correction** is generally not needed for mostly spherical atomized powders when reporting an equivalent-sphere Q₃, but the assumption must be stated. For the small fraction of irregular or agglomerated particles, the volume approximation d³ introduces systematic error; these should be flagged and their impact assessed by sensitivity analysis. Always **report both Q₀ and model-derived Q₃** and label Q₃ explicitly as assuming equal-density equivalent spheres.

## 7. SEM Image Analysis vs. Laser Diffraction and Sieving

Grubbs et al. (2021) compared laser diffraction (LD) and static image analysis (SIA) across four AM powders and found **substantial method-dependent differences** in D10, D50, and D90 (grubbs2021comparisonoflaser pages 9-10, grubbs2021comparisonoflaser pages 13-14, grubbs2021comparisonoflaser pages 12-13):

- **SIA generally underestimates particle diameter** relative to LD, particularly for irregular particles, and tends to report more fine particles and fewer large particles.
- **LD broadens distributions** due to smoothing algorithms, increasing apparent intermediate-size material, generally raising D10 while lowering D90 relative to a reference distribution.
- The fundamental **weighting difference** (SIA measures number-based Q₀; LD measures volume-based Q₃) means their percentile values are not directly equivalent.
- **Fine particles below ~20 µm** showed the greatest cross-method inconsistency (grubbs2021comparisonoflaser pages 12-13, grubbs2021comparisonoflaser pages 1-2).
- Combined LD-dynamic image analysis systems can provide both PSD and morphology, though results vary with carrier fluid, flow rate, and instrument settings (grubbs2021comparisonoflaser pages 2-2).

**Systematic reasons for discrepancies include:** 2D projection effects (SEM measures a projected area, not the true 3D volume); preferred orientation of non-spherical particles; size segregation and sedimentation on the stub; fines adhering to coarse particles or hidden as satellites; agglomerate state (dispersed vs. intact); LD assumptions of sphericity and Mie/Fraunhofer optical models; and sieve analysis measuring the minimum passing dimension rather than a projected area.

**Dynamic image analysis** (Camsizer, QICPIC, Morphologi 4) combines high throughput with simultaneous size and shape information and serves as a useful reference method, though results depend on dispersion method, carrier fluid, and the exact size definition used (grubbs2021comparisonoflaser pages 13-14, charbonneau2025classificationofmetallic pages 12-14).

## 8. Satellites and Agglomerates

Satellite particles and agglomerates can be quantified from SEM images using shape-descriptor thresholds. Charbonneau et al. (2025) used **convexity (C_x = P_convex/P) below 0.95** (in Clemex) or **below 0.90** (in ImageJ) to flag particles with multiple satellites, and **extent ratio below 0.95** for particles with a single growing satellite (charbonneau2025classificationofmetallic pages 7-10, charbonneau2025classificationofmetallic pages 2-4). These thresholds are software-specific because perimeter algorithms differ: ImageJ convexity values are significantly lower than Clemex values for the same particles (charbonneau2025classificationofmetallic pages 10-12).

**Ultrasonic atomization (UA) vs. gas atomization (GA):** UA powder exhibits higher sphericity (0.88–0.90 vs. 0.76 for GA), narrower PSD (Span 0.37–0.43 vs. 0.81), and fewer satellites (scientific2023comparisonofultrasonic pages 8-10). UA copper powders showed an **absence of satellites** (Cabrioli et al. 2025), while GA powders consistently showed satellite particles and some irregular particles (hinrichs2021flexiblepowderproduction pages 7-9, zhang2026gasatomizationfor pages 5-7). The satellite index increases with higher melt temperature during UA (ren2026ambientatmosphereultrasonicatomization pages 6-11, yang2026effectsofultrasonic pages 11-16). Li et al. (2023) note that true satellite attachment cannot be definitively established from 2D SEM images because the physical connection is not directly observable (li2023automaticcharacterizationof pages 12-15).

**Report:** particle fraction with satellites, satellite count per parent (where separable), satellite-to-parent diameter ratio, and the fraction of irregular/agglomerated particles, with thresholds calibrated to the specific alloy and software.

## 9. Imaging Practice

**SE vs. BSE detector:** For automated segmentation of metal powder on carbon tape, the **backscattered-electron (BSE) detector is preferred** because it provides Z-contrast: high-atomic-number Cu-alloy particles appear bright against low-Z carbon with minimal topographic interference from the rough tape surface. Giunto et al. (2026) demonstrated that BSE at 15 kV enables robust threshold-based segmentation of powder on carbon tape (giunto2026accuratesemedsquantification pages 15-17). The SE (ETD) detector provides superior topographic detail for satellite identification and surface texture assessment but produces higher noise from tape roughness, making automated threshold segmentation less reliable.

**Dispersion:** Dry sprinkling from a spatula or through a validated dry disperser, targeting sparse monolayer coverage (<10% area coverage), with excess tapped off. Avoid solvent suspension unless validated, as it can cause preferential sedimentation of fines and size segregation on the stub. Prepare multiple stubs from independent splits.

**Magnification ladder:** For a size range spanning >1 decade (10–260 µm), use at least **three tiers**: ~75× (overview, large particles), ~200× (main 50–200 µm DED range), and ~500× (fines <50 µm and shape). Analyze each tier only over its validated size interval and reconcile overlaps between tiers.

**Fields and stubs:** Use at least three independent stubs from independent splits, with a systematic-random stage grid (not operator-selected "interesting" fields). The total number of fields should accumulate ≥1,000 particles for the primary PSD and ≥10,000 for morphology (wouters2025assessingparticlecount pages 2-3, wouters2025assessingparticlecount pages 7-9).

## 10. Reporting Conventions

A compliant report must state: lot and split provenance; stub preparation method; SEM model, detector, voltage, working distance, and field-selection scheme; calibration standard and uncertainty; magnification, field dimensions, and µm/px by tier; accepted and rejected particle counts by field, stub, tier, and size class; segmentation software, version, parameters, and perimeter estimator; validation metrics (precision, recall, IoU/AJI+, size bias); edge, duplicate, occlusion, and lower-cutoff exclusion rules; descriptor definitions and formulas; cumulative Q₀ and model-derived Q₃ curves; D10, D50, D90 with 95% bootstrap confidence intervals; span = (D90−D10)/D50; shape-descriptor histograms; satellite and agglomerate fractions; and representative raw/mask overlays.

**Shape descriptor definitions per ISO 9276-6:**
- **Circularity:** C = 4πA/P² (ranges 0–1; equals 1 for a perfect circle). Note: some sources use the square-root form √(4πA/P²).
- **Aspect ratio:** Feret_min/Feret_max or minor/major axis of fitted ellipse.
- **Solidity:** A/A_convex-hull.
- **Convexity:** P_convex-hull/P (charbonneau2025classificationofmetallic pages 2-4).

State which formula is used, as published values are not comparable across definitions (charbonneau2025classificationofmetallic pages 14-16, charbonneau2025classificationofmetallic pages 7-10).

---

## Recommended Protocol for the Next Powder Lot

The following numbered protocol covers all steps from sample splitting through reporting:

| Step | Step name | Details/specifications |
|---:|---|---|
| 1 | Representative splitting | Sample the homogenized lot and reduce it according to ISO 14488 using a rotary sample divider; prepare at least three independent final splits for separate stubs. Record lot mass, splitter, division sequence, split masses and retained archive sample. Do not scoop only from the container surface. |
| 2 | Stub preparation | Apply fresh conductive carbon tape. Deposit each independent split as a sparse monolayer by controlled dry sprinkling from a clean spatula or through a validated dry disperser; tap off unattached powder. Target less than about 10% projected-area coverage and at least one particle diameter of separation for most particles. Prepare additional stubs rather than accepting dense multilayers. Carbon-tape mounting supports automated powder analysis (giunto2026accuratesemedsquantification pages 3-5). |
| 3 | Detector and beam conditions | Acquire registered BSE and ETD-SE images at 15–20 kV, fixed working distance, dwell time and contrast settings. Use BSE as the quantitative segmentation channel because Cu-alloy particles are bright against low-Z carbon with less tape-topography contrast; retain SE for satellites, surface texture and morphology review (giunto2026accuratesemedsquantification pages 15-17). |
| 4 | Magnification ladder | Use approximately 75× for overview and particles up to about 260 µm; approximately 200× for the principal 50–200 µm DED range; and approximately 500× for particles below 50 µm, satellites and shape. Select fields by a predefined systematic-random stage grid, not by visual attractiveness. Analyze each tier only over its validated size interval and reconcile overlaps between tiers. |
| 5 | Pixel-size targets | Verify the actual calibrated sampling at every tier. Target no more than 0.5 µm/px for the principal PSD tier and no more than 0.2 µm/px for fines and morphology. Keep acquisition settings constant within a tier. Resolution changes measured perimeter and therefore circularity and convexity (charbonneau2025classificationofmetallic pages 12-14). |
| 6 | Fields and counts | Acquire fields across all three independent stubs and splits: initially at least 20 overview, 30 main-tier and 30 fine-tier fields, increasing these until precision targets are met. Obtain at least 1,000 accepted particles for the primary Q0 PSD and aim for at least 10,000 accepted particles for robust morphology and model-derived Q3 tails. Report accepted and rejected counts by field, stub, tier and size class; tail percentiles require more observations than the median (wouters2025assessingparticlecount pages 2-3, wouters2025assessingparticlecount pages 7-9). |
| 7 | Calibration and traceability | At the session start and end, calibrate x and y scale using a traceable stage micrometer or certified reference particles covering the relevant size range. Record certificate, uncertainty, date, SEM settings and measured scale error; verify pixel aspect ratio and stage drift. Certified cross-gratings or reference particles are established calibration routes (kestens2014certificationreportthecertification pages 76-76, kestens2014certificationreportthecertification pages 75-76). |
| 8 | Segmentation | Segment the BSE channel using flat-field correction, global Otsu thresholding where contrast is uniform or validated local thresholding otherwise, hole filling and removal of scale bars/text. Separate light contacts using distance-transform marker-controlled watershed with documented h-maxima or minimum-peak-distance settings. Use a locally fine-tuned instance model—preferably uncertainty-aware Mask R-CNN—for severe overlap, then measure the retained masks rather than fitted circles. Watershed showed 99.3% precision but only 89.2% recall on dense powder SEM images, while a powder-specific hybrid reached 99.3% precision and 99.5% recall (li2023automaticcharacterizationof pages 9-12, rettenberger2024uncertaintyawareparticlesegmentation pages 3-4). |
| 9 | Validation and acceptance | Create an independently annotated, stratified validation set containing at least 50 hand-measured particles and preferably 200 or more instances across size classes, stubs, detectors, satellites, irregular particles, touching pairs and severe overlaps. Compare automated and manual equivalent diameters with identity/Bland–Altman plots and report precision, recall, split rate, merge rate and mask IoU/AJI+. Provisional acceptance: absolute mean diameter bias below 2%, median absolute relative error below 5%, precision and recall at least 0.95, and no significant size-dependent bias; otherwise correct and revalidate. Expert disagreement itself can be substantial, so preserve annotation rules and adjudication records (rettenberger2024uncertaintyawareparticlesegmentation pages 5-6, rettenberger2024uncertaintyawareparticlesegmentation pages 3-4). |
| 10 | Edges, duplicates and occlusion | Prefer an unbiased inclusion frame: include particles intersecting the top and left acceptance lines but exclude those intersecting the bottom and right forbidden lines. If all frame-touching particles are discarded, report that rule and apply Miles–Lantuéjoul weighting, using particle-specific x/y extents when possible; for approximately isotropic extent d, use w = WH/[(W−d)(H−d)]. Remove duplicate particles in overlapping fields by stage coordinates or mask matching. Exclude strongly occluded particles from size and shape unless the hidden contour is validated; report them separately. Border-particle removal avoids partial-visibility bias (yildirim2021bayesianparticleinstance pages 9-11), while overlapping internal tiles can be reconciled by mask merging (yichao2021particleautostatisticsand pages 4-6). |
| 11 | Size and shape measurements | Use projected-area-equivalent circle diameter dA = 2√(A/π) as the primary size; also report Feret maximum and minimum. Report circularity C = 4πA/P², aspect ratio = Feret min/Feret max or fitted-ellipse minor/major axis, solidity = A/Aconvex-hull and convexity = Pconvex-hull/P. State the exact convention, thresholding and Crofton or corrected chain-code perimeter estimator; software perimeter differences of 3–5% have been observed (charbonneau2025classificationofmetallic pages 4-7, charbonneau2025classificationofmetallic pages 7-10). |
| 12 | Lower size cutoff | Establish cutoffs by calibrated pixel occupancy and validation. For size, require at least 10 px across and at least about 100 foreground pixels; for perimeter-based morphology, use at least 1,000 pixels where practicable and preferably about 3,000 pixels. ISO-related guidance cited in the literature is approximately 100–5,000 pixels per particle (charbonneau2025classificationofmetallic pages 12-14, charbonneau2025classificationofmetallic pages 4-7). Thus at 0.5 µm/px the provisional size cutoff is 5 µm, and at 0.2 µm/px it is 2 µm; morphology cutoffs will be larger and must be reported separately. |
| 13 | Number-to-volume conversion | Retain the measured number-weighted Q0 distribution as primary. For an equivalent-sphere Q3 estimate, assign each accepted particle weight wi = dA,i³ and calculate Q3(d) = Σ(dA,i³·I[dA,i≤d])/ΣdA,i³ in accordance with the ISO 9276-2 moment concept. Bootstrap whole fields or stubs, not isolated particles, and report Q0 and model-derived Q3 separately; the cubic weighting makes Q3 and especially D90 sensitive to rare large particles (grubbs2021comparisonoflaser pages 13-14, grubbs2021comparisonoflaser pages 2-2). |
| 14 | Satellites and agglomerates | Preserve the original connected mask before watershed and classify parent particles as no satellite, one satellite, multiple satellites, irregular or agglomerated. Use convexity below 0.95 and extent ratio below about 0.95 only as provisional flags, followed by manual audit and locally optimized thresholds. Published thresholds vary with software—for example, convexity 0.95 in Clemex versus 0.90 in ImageJ—because perimeter implementations differ (charbonneau2025classificationofmetallic pages 7-10, charbonneau2025classificationofmetallic pages 2-4). Report particle fraction with satellites, satellite count per parent and, where separable, satellite-to-parent diameter ratio. |
| 15 | Reporting | Report lot and split provenance; stub preparation; SEM, detector, voltage, working distance and field-selection scheme; calibration and uncertainty; magnification, field size and µm/px by tier; accepted/rejected counts and n per size class; segmentation software, version and parameters; validation metrics; edge, duplicate, occlusion and lower-cutoff rules; descriptor equations and perimeter estimator; cumulative Q0 and model-derived Q3 curves; D10, D50, D90 and span = (D90−D10)/D50 with field/stub bootstrap 95% confidence intervals; shape histograms; satellite/agglomerate fractions; and representative raw/mask overlays. State explicitly that Q3 assumes equal-density equivalent spheres and compare it separately with ASTM B822 laser diffraction and ASTM B214 sieve results (grubbs2021comparisonoflaser pages 9-10, grubbs2021comparisonoflaser pages 13-14, moroni2020onstandardizationefforts pages 9-12). |


*Table: A numbered acquisition, segmentation, validation and reporting protocol for quantitative particle-size and morphology analysis of the next C63000 powder lot on the Apreo C.*

---

## Current Choices That Would Not Meet ISO 13322-1

Based on the evidence gathered, the following aspects of the current approach would not satisfy ISO 13322-1 requirements:

1. **Single sprinkled stub from one portion:** ISO 14488 and ISO 13322-1 require representative sampling through documented splitting. One conveniently selected portion on one stub does not establish lot representativeness.

2. **Densely packed monolayer with many touching/overlapping particles:** ISO 13322-1 requires adequate dispersion. Dense packing makes segmentation unreliable and introduces systematic bias from occlusion and merging errors.

3. **Single magnification tier (133–200×) for a >1-decade size range:** At 0.67–1.01 µm/px, fines below ~10 µm contain fewer than 100 pixels and cannot yield reliable size or shape data per the ISO 9276-6 guideline of 100–5000 pixels per particle (charbonneau2025classificationofmetallic pages 12-14). A magnification ladder is required.

4. **SE (ETD) detector alone for segmentation:** While SE images provide excellent topographic detail, BSE provides far more robust compositional contrast for automated threshold segmentation on carbon tape (giunto2026accuratesemedsquantification pages 15-17). At minimum, acquire registered BSE images as the primary segmentation channel.

5. **Naive Hough-circle detection without validated segmentation:** The thousands of false circles per field confirm that this approach is not a validated segmentation method. ISO 13322-1 requires documented, validated segmentation with stated accuracy.

6. **No documented calibration:** A traceable stage micrometer or certified reference beads must be imaged and the scale verified at each session, with certificate, uncertainty, and measured scale error recorded (kestens2014certificationreportthecertification pages 76-76, kestens2014certificationreportthecertification pages 75-76).

7. **Insufficient particle counts for volume-weighted percentiles:** With only nine fields and dense packing causing segmentation failures, the accepted particle count is unlikely to reach the ≥1,000 needed for a reliable number-weighted PSD, let alone the ≥10,000 desirable for volume-weighted tails and robust morphology.

8. **No stated edge-exclusion or occlusion rule:** Particles touching the frame must be handled by an unbiased frame or excluded with Miles–Lantuéjoul correction; occluded particles must be flagged and treated consistently (yildirim2021bayesianparticleinstance pages 9-11).

In summary, the current setup provides a useful starting dataset but requires representative lot splitting, sparse dispersion on multiple stubs, BSE acquisition alongside SE, a three-tier magnification ladder, traceable calibration, validated instance segmentation (preferably fine-tuned Mask R-CNN with watershed baseline), documented edge and occlusion rules, and a substantially larger particle count before the results can be reported as an ISO 13322-1–conforming particle-size and morphology characterization.

References

1. (kestens2014certificationreportthecertification pages 76-76): V KESTENS and G ROEBBEN. Certification report-the certification of equivalent diameters of a mixture of silica nanoparticles in aqueous solution: erm®-fd102. Unknown journal, 2014.

2. (grubbs2021comparisonoflaser pages 3-5): Jack Grubbs, Kyle Tsaknopoulos, Christopher Massar, Benjamin Young, Anna O'Connell, Caitlin Walde, Aaron Birt, Matthew Siopis, and Danielle Cote. Comparison of laser diffraction and image analysis techniques for particle size-shape characterization in additive manufacturing applications. Powder Technology, 391:20-33, Oct 2021. URL: https://doi.org/10.1016/j.powtec.2021.06.003, doi:10.1016/j.powtec.2021.06.003. This article has 87 citations and is from a domain leading peer-reviewed journal.

3. (charbonneau2025classificationofmetallic pages 12-14): Cindy Charbonneau, Fabrice Bernier, Étienne Perrault, Roger Pelletier, and Louis-Philippe Lefebvre. Classification of metallic powder morphology using traditional and automated static image analysis: a comparative study. Powders, 4:15, May 2025. URL: https://doi.org/10.3390/powders4020015, doi:10.3390/powders4020015. This article has 6 citations.

4. (charbonneau2025classificationofmetallic pages 4-7): Cindy Charbonneau, Fabrice Bernier, Étienne Perrault, Roger Pelletier, and Louis-Philippe Lefebvre. Classification of metallic powder morphology using traditional and automated static image analysis: a comparative study. Powders, 4:15, May 2025. URL: https://doi.org/10.3390/powders4020015, doi:10.3390/powders4020015. This article has 6 citations.

5. (charbonneau2025classificationofmetallic pages 14-16): Cindy Charbonneau, Fabrice Bernier, Étienne Perrault, Roger Pelletier, and Louis-Philippe Lefebvre. Classification of metallic powder morphology using traditional and automated static image analysis: a comparative study. Powders, 4:15, May 2025. URL: https://doi.org/10.3390/powders4020015, doi:10.3390/powders4020015. This article has 6 citations.

6. (moroni2020onstandardizationefforts pages 9-12): Giovanni Moroni, Stefano Petrò, and Huan Shao. On standardization efforts for additive manufacturing. Lecture Notes in Mechanical Engineering, pages 156-172, Jan 2020. URL: https://doi.org/10.1007/978-3-030-46212-3\_11, doi:10.1007/978-3-030-46212-3\_11. This article has 25 citations and is from a peer-reviewed journal.

7. (charbonneau2025classificationofmetallic pages 1-2): Cindy Charbonneau, Fabrice Bernier, Étienne Perrault, Roger Pelletier, and Louis-Philippe Lefebvre. Classification of metallic powder morphology using traditional and automated static image analysis: a comparative study. Powders, 4:15, May 2025. URL: https://doi.org/10.3390/powders4020015, doi:10.3390/powders4020015. This article has 6 citations.

8. (wouters2025assessingparticlecount pages 2-3): Charlotte Wouters, Vikram Kestens, Eveline Verleysen, and Jan Mast. Assessing particle count in electron microscopy measurements of nanomaterials to support regulatory guidance. Scientific Reports, Apr 2025. URL: https://doi.org/10.1038/s41598-025-92266-4, doi:10.1038/s41598-025-92266-4. This article has 24 citations and is from a peer-reviewed journal.

9. (grubbs2021comparisonoflaser pages 13-14): Jack Grubbs, Kyle Tsaknopoulos, Christopher Massar, Benjamin Young, Anna O'Connell, Caitlin Walde, Aaron Birt, Matthew Siopis, and Danielle Cote. Comparison of laser diffraction and image analysis techniques for particle size-shape characterization in additive manufacturing applications. Powder Technology, 391:20-33, Oct 2021. URL: https://doi.org/10.1016/j.powtec.2021.06.003, doi:10.1016/j.powtec.2021.06.003. This article has 87 citations and is from a domain leading peer-reviewed journal.

10. (grubbs2021comparisonoflaser pages 2-2): Jack Grubbs, Kyle Tsaknopoulos, Christopher Massar, Benjamin Young, Anna O'Connell, Caitlin Walde, Aaron Birt, Matthew Siopis, and Danielle Cote. Comparison of laser diffraction and image analysis techniques for particle size-shape characterization in additive manufacturing applications. Powder Technology, 391:20-33, Oct 2021. URL: https://doi.org/10.1016/j.powtec.2021.06.003, doi:10.1016/j.powtec.2021.06.003. This article has 87 citations and is from a domain leading peer-reviewed journal.

11. (grubbs2021comparisonoflaser pages 1-2): Jack Grubbs, Kyle Tsaknopoulos, Christopher Massar, Benjamin Young, Anna O'Connell, Caitlin Walde, Aaron Birt, Matthew Siopis, and Danielle Cote. Comparison of laser diffraction and image analysis techniques for particle size-shape characterization in additive manufacturing applications. Powder Technology, 391:20-33, Oct 2021. URL: https://doi.org/10.1016/j.powtec.2021.06.003, doi:10.1016/j.powtec.2021.06.003. This article has 87 citations and is from a domain leading peer-reviewed journal.

12. (batistao2026surfacefunctionalizationof pages 69-73): BF Batistão. Surface functionalization of the aa2017 aluminum alloy powder for use in additive manufacturing. Unknown journal, 2026.

13. (kestens2014certificationreportthecertification pages 75-76): V KESTENS and G ROEBBEN. Certification report-the certification of equivalent diameters of a mixture of silica nanoparticles in aqueous solution: erm®-fd102. Unknown journal, 2014.

14. (wouters2025assessingparticlecount pages 7-9): Charlotte Wouters, Vikram Kestens, Eveline Verleysen, and Jan Mast. Assessing particle count in electron microscopy measurements of nanomaterials to support regulatory guidance. Scientific Reports, Apr 2025. URL: https://doi.org/10.1038/s41598-025-92266-4, doi:10.1038/s41598-025-92266-4. This article has 24 citations and is from a peer-reviewed journal.

15. (wouters2025assessingparticlecount pages 4-6): Charlotte Wouters, Vikram Kestens, Eveline Verleysen, and Jan Mast. Assessing particle count in electron microscopy measurements of nanomaterials to support regulatory guidance. Scientific Reports, Apr 2025. URL: https://doi.org/10.1038/s41598-025-92266-4, doi:10.1038/s41598-025-92266-4. This article has 24 citations and is from a peer-reviewed journal.

16. (charbonneau2025classificationofmetallic pages 7-10): Cindy Charbonneau, Fabrice Bernier, Étienne Perrault, Roger Pelletier, and Louis-Philippe Lefebvre. Classification of metallic powder morphology using traditional and automated static image analysis: a comparative study. Powders, 4:15, May 2025. URL: https://doi.org/10.3390/powders4020015, doi:10.3390/powders4020015. This article has 6 citations.

17. (charbonneau2025classificationofmetallic pages 10-12): Cindy Charbonneau, Fabrice Bernier, Étienne Perrault, Roger Pelletier, and Louis-Philippe Lefebvre. Classification of metallic powder morphology using traditional and automated static image analysis: a comparative study. Powders, 4:15, May 2025. URL: https://doi.org/10.3390/powders4020015, doi:10.3390/powders4020015. This article has 6 citations.

18. (giunto2026accuratesemedsquantification pages 15-17): A. Giunto, Yu-Xing Fei, Pragnay Nevatia, Bernardus Rendy, N. Szymanski, and G. Ceder. Accurate sem-eds quantification, automation, and machine learning enable high-throughput compositional characterization of powders. Nature Communications, Aug 2026. URL: https://doi.org/10.1038/s41467-026-76633-x, doi:10.1038/s41467-026-76633-x. This article has 6 citations and is from a highest quality peer-reviewed journal.

19. (li2023automaticcharacterizationof pages 9-12): X Li, L Cui, and S Shonkwiler. Automatic characterization of spherical metal powders by microscope. Unknown journal, 2023.

20. (li2023automaticcharacterizationof pages 12-15): X Li, L Cui, and S Shonkwiler. Automatic characterization of spherical metal powders by microscope. Unknown journal, 2023.

21. (li2023automaticcharacterizationof pages 1-5): X Li, L Cui, and S Shonkwiler. Automatic characterization of spherical metal powders by microscope. Unknown journal, 2023.

22. (yichao2021particleautostatisticsand pages 1-3): W Yichao, Z Zheng, and H Haizhou. Particle auto-statistics and measurement of the spherical powder for 3d printing based on deep learning. Unknown journal, 2021.

23. (yichao2021particleautostatisticsand pages 7-9): W Yichao, Z Zheng, and H Haizhou. Particle auto-statistics and measurement of the spherical powder for 3d printing based on deep learning. Unknown journal, 2021.

24. (yichao2021particleautostatisticsanda pages 3-4): W Yichao, Z Zheng, and H Haizhou. Particle auto-statistics and measurement of the spherical powder for 3d printing based on deep learning. Unknown journal, 2021.

25. (rettenberger2024uncertaintyawareparticlesegmentation pages 3-4): Luca Rettenberger, Nathan J. Szymanski, Yan Zeng, Jan Schuetzke, Shilong Wang, Gerbrand Ceder, and Markus Reischl. Uncertainty-aware particle segmentation for electron microscopy at varied length scales. npj Computational Materials, 10:1-9, Jun 2024. URL: https://doi.org/10.1038/s41524-024-01302-w, doi:10.1038/s41524-024-01302-w. This article has 27 citations and is from a peer-reviewed journal.

26. (rettenberger2024uncertaintyawareparticlesegmentation pages 4-5): Luca Rettenberger, Nathan J. Szymanski, Yan Zeng, Jan Schuetzke, Shilong Wang, Gerbrand Ceder, and Markus Reischl. Uncertainty-aware particle segmentation for electron microscopy at varied length scales. npj Computational Materials, 10:1-9, Jun 2024. URL: https://doi.org/10.1038/s41524-024-01302-w, doi:10.1038/s41524-024-01302-w. This article has 27 citations and is from a peer-reviewed journal.

27. (rettenberger2024uncertaintyawareparticlesegmentation pages 2-3): Luca Rettenberger, Nathan J. Szymanski, Yan Zeng, Jan Schuetzke, Shilong Wang, Gerbrand Ceder, and Markus Reischl. Uncertainty-aware particle segmentation for electron microscopy at varied length scales. npj Computational Materials, 10:1-9, Jun 2024. URL: https://doi.org/10.1038/s41524-024-01302-w, doi:10.1038/s41524-024-01302-w. This article has 27 citations and is from a peer-reviewed journal.

28. (yildirim2021bayesianparticleinstance pages 7-8): Batuhan Yildirim and Jacqueline M. Cole. Bayesian particle instance segmentation for electron microscopy image quantification. Journal of Chemical Information and Modeling, 61:1136-1149, Mar 2021. URL: https://doi.org/10.1021/acs.jcim.0c01455, doi:10.1021/acs.jcim.0c01455. This article has 69 citations and is from a peer-reviewed journal.

29. (yildirim2021bayesianparticleinstance pages 9-11): Batuhan Yildirim and Jacqueline M. Cole. Bayesian particle instance segmentation for electron microscopy image quantification. Journal of Chemical Information and Modeling, 61:1136-1149, Mar 2021. URL: https://doi.org/10.1021/acs.jcim.0c01455, doi:10.1021/acs.jcim.0c01455. This article has 69 citations and is from a peer-reviewed journal.

30. (yichao2021particleautostatisticsanda pages 1-3): W Yichao, Z Zheng, and H Haizhou. Particle auto-statistics and measurement of the spherical powder for 3d printing based on deep learning. Unknown journal, 2021.

31. (yichao2021particleautostatisticsand pages 4-6): W Yichao, Z Zheng, and H Haizhou. Particle auto-statistics and measurement of the spherical powder for 3d printing based on deep learning. Unknown journal, 2021.

32. (yichao2021particleautostatisticsanda pages 4-6): W Yichao, Z Zheng, and H Haizhou. Particle auto-statistics and measurement of the spherical powder for 3d printing based on deep learning. Unknown journal, 2021.

33. (grubbs2021comparisonoflaser pages 9-10): Jack Grubbs, Kyle Tsaknopoulos, Christopher Massar, Benjamin Young, Anna O'Connell, Caitlin Walde, Aaron Birt, Matthew Siopis, and Danielle Cote. Comparison of laser diffraction and image analysis techniques for particle size-shape characterization in additive manufacturing applications. Powder Technology, 391:20-33, Oct 2021. URL: https://doi.org/10.1016/j.powtec.2021.06.003, doi:10.1016/j.powtec.2021.06.003. This article has 87 citations and is from a domain leading peer-reviewed journal.

34. (grubbs2021comparisonoflaser pages 12-13): Jack Grubbs, Kyle Tsaknopoulos, Christopher Massar, Benjamin Young, Anna O'Connell, Caitlin Walde, Aaron Birt, Matthew Siopis, and Danielle Cote. Comparison of laser diffraction and image analysis techniques for particle size-shape characterization in additive manufacturing applications. Powder Technology, 391:20-33, Oct 2021. URL: https://doi.org/10.1016/j.powtec.2021.06.003, doi:10.1016/j.powtec.2021.06.003. This article has 87 citations and is from a domain leading peer-reviewed journal.

35. (charbonneau2025classificationofmetallic pages 2-4): Cindy Charbonneau, Fabrice Bernier, Étienne Perrault, Roger Pelletier, and Louis-Philippe Lefebvre. Classification of metallic powder morphology using traditional and automated static image analysis: a comparative study. Powders, 4:15, May 2025. URL: https://doi.org/10.3390/powders4020015, doi:10.3390/powders4020015. This article has 6 citations.

36. (scientific2023comparisonofultrasonic pages 8-10): International Scientific, B. Bałasz, M. Bielecki, W. Gulbiński, and Ł. Słoboda. Comparison of ultrasonic and other atomization methods in metal powder production. Journal of Achievements in Materials and Manufacturing Engineering, 116:11-24, Jan 2023. URL: https://doi.org/10.5604/01.3001.0016.3393, doi:10.5604/01.3001.0016.3393. This article has 38 citations.

37. (hinrichs2021flexiblepowderproduction pages 7-9): Frauke Hinrichs, Alexander Kauffmann, Daniel Schliephake, Sascha Seils, Susanne Obert, Karin Ratschbacher, Melissa Allen, Astrid Pundt, and Martin Heilmaier. Flexible powder production for additive manufacturing of refractory metal-based alloys. Metals, 11:1723, Oct 2021. URL: https://doi.org/10.3390/met11111723, doi:10.3390/met11111723. This article has 27 citations.

38. (zhang2026gasatomizationfor pages 5-7): Chao-Cai Zhang, Fu-Zhong Chu, and Zong-Yan Zhou. Gas atomization for metal powder production in additive manufacturing: a review. Materials Science in Additive Manufacturing, 0:026220051, Sep 2026. URL: https://doi.org/10.36922/msam026220051, doi:10.36922/msam026220051. This article has 0 citations and is from a peer-reviewed journal.

39. (ren2026ambientatmosphereultrasonicatomization pages 6-11): Ding-Ying Ren, Hao-Di Li, Xiao-Feng Yang, Hao Lan, Xiao-Qiang Hu, Peng Yu, and Qian Wang. Ambient-atmosphere ultrasonic atomization of low-melting-point wood’s alloy powders: process optimization, atomization mechanism, and solderability. Journal of Materials Science: Materials in Electronics, Oct 2026. URL: https://doi.org/10.1007/s10854-026-18601-1, doi:10.1007/s10854-026-18601-1. This article has 0 citations and is from a peer-reviewed journal.

40. (yang2026effectsofultrasonic pages 11-16): Xiao-Feng Yang, Hao-Di Li, Ding-Ying Ren, Hao Lan, Xiao-Qiang Hu, Qian Wang, and Peng Yu. Effects of ultrasonic atomization parameters on the properties of sn-58bi powder and its application in ultrasonic-assisted soldering. Journal of Materials Science: Materials in Electronics, Oct 2026. URL: https://doi.org/10.1007/s10854-026-18683-x, doi:10.1007/s10854-026-18683-x. This article has 0 citations and is from a peer-reviewed journal.

41. (giunto2026accuratesemedsquantification pages 3-5): A. Giunto, Yu-Xing Fei, Pragnay Nevatia, Bernardus Rendy, N. Szymanski, and G. Ceder. Accurate sem-eds quantification, automation, and machine learning enable high-throughput compositional characterization of powders. Nature Communications, Aug 2026. URL: https://doi.org/10.1038/s41467-026-76633-x, doi:10.1038/s41467-026-76633-x. This article has 6 citations and is from a highest quality peer-reviewed journal.

42. (rettenberger2024uncertaintyawareparticlesegmentation pages 5-6): Luca Rettenberger, Nathan J. Szymanski, Yan Zeng, Jan Schuetzke, Shilong Wang, Gerbrand Ceder, and Markus Reischl. Uncertainty-aware particle segmentation for electron microscopy at varied length scales. npj Computational Materials, 10:1-9, Jun 2024. URL: https://doi.org/10.1038/s41524-024-01302-w, doi:10.1038/s41524-024-01302-w. This article has 27 citations and is from a peer-reviewed journal.
