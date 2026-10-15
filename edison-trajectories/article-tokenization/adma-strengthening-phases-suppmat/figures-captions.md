<!-- Extracted from Edison tokenization of adma70703-sup-0001-suppmat.pdf -->

## FIGURES
Figure 1: Fig. S1. Flow diagram and design approaches for measuring structure parameters. The composition is inversely designed for the primary goal of minimizing the coarsening metric of L12 phases. All other microstructural features are forward predicted and work as constraints for the inversely designed composition.
Figure 2: Fig. S2. Root mean square error (RMSE) of the normalized coarsening metric with respect to the training data % for six applied ML techniques: neural network (NN), K-nearest neighbor (KNN), random forest (RF), support vector machine (SVM), gradient boost (GB), and linear regression (LR) techniques. A minimum of 40 samples is required to achieve < 3% of error to predict the entire compositional space for the most efficient algorithm, NN. For NN the simulation was repeated for ten random initial seeds and the standard deviation is shown.
Figure 3: Fig. S3. CALPHAD simulation of phase molar percentage with respect to temperature for the designed Al-Er-Zr-Ni alloy.
Figure 4: Fig. S4. Distribution of concentrations for alloying elements and normalized target properties (i.e., L12, diffusion resistivity, misfit strain (ε), and coarsening metric) for 500,000 random compositions. Target properties are normalized with associated values from the benchmark printable Al alloy. Coarsening metrics > 4 are assigned to 4.
Figure 5: Fig. S5. Distribution of diffusion resistivity with respect to studied parameters. Increasing Zr has the greatest influence on increasing diffusion resistivity.
Figure 6: Fig. S6. Distribution of misfit strain (ε) with respect to studied parameters. Low coarsening metrics have low misfit strain and Zr is the main contributor.
Figure 7: Fig. S7. Distribution of coarsening metric with respect to studied parameters. Increasing Zr has the most significant contribution to reduce the coarsening metric.
Figure 8: Fig. S8. Distribution of L12 with respect to studied parameters. Increasing Er has the greatest influence on the L12 content.
Figure 9: Fig. S9. a-l) Distribution of microstructural features/material descriptors for different design scenarios. The optimal value obtained via BO using objective functions constructed with only printability parameters (CSC, FR, and HCS) or combinations of these parameters with performance metrics (FR* & CSC*). Data were normalized against corresponding values in the benchmark design. d) CSC, f) HCS, i) Al3Y D019 (mol %), and l) Ternary (mol %) were not normalized as they were found to be zero in the benchmark design. ML-optimized design is plotted for each distribution as a vertical dashed line. Points are colored with coarsening metric, with blue being low and pink being high.
Figure 10: Fig. S10. Histogram of the a) coarsening metric and b) L12 of 1250 designs varied from the ML-optimized design by up to 50% change in composition, normalized against the ML-optimized design. Both descriptors are highly stable under these variations.
Figure 11: Fig. S11. Contour plot of a) freezing range (FR), b) cracking susceptibility coefficient (CSC), and c) hot cracking susceptibility (HCS) for various Ni and Zr concentrations.
Figure 12: Fig. S12. Results of Vickers hardness testing on a) as-built and b) aged samples with different Ni and Zr concentrations. In both figures, the dashed lines define the min Ni concentration to have maximum ternary phase.
Figure 13: Fig. S13. a, c) SEM images and b, d) their corresponding EDS maps. e, f, g) Size distribution of Al3Zr, Al3Ni, and ternary precipitates from various SEM images at resolution presented in (c) adapted from ref.14.
Figure 14: Fig. S14. Higher magnification STEM EDS dataset. a) HAADF overview of the imaged grain along a <110>-type zone indicating regions of interest for which the b) composition maps are averaged and summarized in (c).
Figure 15: Fig. S15. SEM-EDS images of induction-melted sample from the optimized composition. Micro-scale phases which are rich in Er and Ni contents are seen in these images.
Figure 16: Fig. S16. SEM-EDS image of the sample with Al-0.4Er-1Zr-0Ni composition. Clusters of micro-scale Zr-rich areas are seen in some grains of this sample.
Figure 17: Fig. S17. Distribution of the hardness for experimented samples from ML-optimized design (Al-Er-Zr-Ni), wrought Al 7075, and the benchmark alloy (Al-Er-Zr-Y-Yb-Ni).
Figure 18: Fig. S18. Induction melted samples after multiple laser path scanning. No cracks were detected in melted areas (above dashed lines). These four samples are the four left down diamonds in Fig. S11.
Figure 19: Fig. S19. STEM EDS maps of matrix and L12 nanoclusters. a) Elemental maps and average composition ratios across the overall matrix (containing L12 nanoclusters). b) Elemental maps and composition ratio for a single L12 nanocluster. The dotted box indicates the averaging area for the elemental quantification.
Figure 20: Fig. S20. Reconstructed 3D models from CT scans of the laser-scanned samples: a) Al-0.4Er-2Zr-0Ni, and b) Al-0.4Er-1Zr-1.33Ni. The laser-scanned layers appear with darker contrast and are annotated accordingly. No cracks or pores were detected throughout these samples. c) CT scans of Al 7075 show high density of long cracks. d, e) Volume percentage of diameter and aspect ratio (short-axis/long-axis) of these defects.
Figure 21: Fig. S21. Area of L12 nanoprecipitates are computed and summarized from Fig. 3i across multiple datasets.
Figure 22: Fig. S22. STEM EDS for the Al3Ni phase. a) HAADF STEM overview, and b) corresponding mask of precipitates consistent with Al3Ni, along with the c) EDS elemental maps reproduced for comparison.

## TABLES
Table 1: Table S1. Hyperparameters which were parametric studied for each regressor to develop the manifold.

| Regression technique | Hyperparameters | Optimum hyperparameters |
|---|---|---|
| Neural network (NN) | # of Conv layers = 1, 2, 3; Conv features = 64, 128, 256; # of FC layers = 2, 3, 4; FC neuron # = 1, 32, 32, 64, 64; Batch size = 32, 64, 128, 256, 512, 1024, 2048; Training loop number = 100, 1000, 10,000, 150,000, 200,000, 300,000; Learning rate = 10-4, 10-3, and 10-2; Regularization factor L1 = 0, 10-6, 10-5; Regularization factor L2 = 0, 10-2, 10-3 | # of Conv layers = 2; Conv features = 64; FC layers = 2; FC neuron # = 32, 1; Batch size = 128; Training loop number = 300,000; Learning rate = 10-3; L1 = 0; L2 = 0 |
| K-nearest-neighbors (KNN) | n_neighbors = 1, 2, 3, 4, 5, 6, 7, 8 | n_neighbors = 7 |
| Support vector machine (SVM) | kernel = 'rbf'; C = 1, 10, 100, 1000 | C = 1000 |
| Random forest (RF) | Max_depth = 2, 4, 6, 8, 10; n_estimators = 20, 40, 60, 80, 100, 120 | Max_depth = 10; n_estimators = 60 |
| Extreme gradient boost (XGB) | Max_depth = 2, 4, 6, 8, 10; num_boost_round = 20, 40, 60, 80, 100, 120 | Max_depth = 10; num_boost_round = 20 |
| Linear regression (LR) |  |  |

Table 2: Table S2. Measured compositions for the matrix, L1$, and ternary phases.

| Composition (wt. fraction) | Al | Er | Zr | Ni |
|---|---:|---:|---:|---:|
| Matrix | 0.9947 | 8.2e-05 | 0.009272 | 0.000543 |
| L1$ | 0.79776 | 0.006912 | 0.193834 | 0.000475 |
| Ternary | 0.68717 | 0.91445 | 0.079137 | 0.138222 |
| Bulk | 0.9218 | 0.0237 | 0.029 | 0.0255 |

Table 3: Table S3. Average composition ratios computed for the masked precipitates and non-precipitate regions from Fig. 2 and Fig. S22.

| Average wt. % | Al | Er | Ni | Zr | Total |
|---|---:|---:|---:|---:|---:|
| Grain boundary precipitates | 79.9 | 7.3 | 8.6 | 4.2 | 100 |
| Non-precipitates | 92.6 | 1.6 | 1.4 | 4.4 | 100 |
| Al3Ni precipitates | 71.5 | 4.7 | 20.2 | 3.6 | 100 |

- Used direct text extraction from the provided PDF rather than OCR because the document text layer was available.
- Preserved visibly corrupted mathematical glyphs and one malformed character sequence (for example in the t-statistic formula and reference 2) rather than guessing missing symbols.
- Mapped supplemental discussion sections into the requested top-level Markdown headings because the source supplemental PDF does not contain a conventional Abstract/Introduction/Methods/Results/Discussion/Conclusions structure.
- Numbered supplemental figures and tables sequentially in the required `Figure N` and `Table N` format while retaining the original `Fig. S#` and `Table S#` labels in captions.

## Extracted figure images (raster objects from PDF)

_40 image object(s) extracted directly from the PDF via `pdfimages`; ordering is by PDF stream order and may not map 1:1 to figure numbers above._

![fig-01.jpg](figures/fig-01.jpg)

![fig-02.jpg](figures/fig-02.jpg)

![fig-03.jpg](figures/fig-03.jpg)

![fig-04.jpg](figures/fig-04.jpg)

![fig-05.jpg](figures/fig-05.jpg)

![fig-06.jpg](figures/fig-06.jpg)

![fig-07.jpg](figures/fig-07.jpg)

![fig-08.jpg](figures/fig-08.jpg)

![fig-09.jpg](figures/fig-09.jpg)

![fig-10.jpg](figures/fig-10.jpg)

![fig-11.jpg](figures/fig-11.jpg)

![fig-12.jpg](figures/fig-12.jpg)

![fig-13.jpg](figures/fig-13.jpg)

![fig-14.jpg](figures/fig-14.jpg)

![fig-15.jpg](figures/fig-15.jpg)

![fig-16.jpg](figures/fig-16.jpg)

![fig-17.jpg](figures/fig-17.jpg)

![fig-18.jpg](figures/fig-18.jpg)

![fig-19.jpg](figures/fig-19.jpg)

![fig-20.jpg](figures/fig-20.jpg)

![fig-21.jpg](figures/fig-21.jpg)

![fig-22.jpg](figures/fig-22.jpg)

![fig-23.jpg](figures/fig-23.jpg)

![fig-24.jpg](figures/fig-24.jpg)

![fig-25.jpg](figures/fig-25.jpg)

![fig-26.jpg](figures/fig-26.jpg)

![fig-27.jpg](figures/fig-27.jpg)

![fig-28.jpg](figures/fig-28.jpg)

![fig-29.jpg](figures/fig-29.jpg)

![fig-30.jpg](figures/fig-30.jpg)

![fig-31.jpg](figures/fig-31.jpg)

![fig-32.jpg](figures/fig-32.jpg)

![fig-33.jpg](figures/fig-33.jpg)

![fig-34.jpg](figures/fig-34.jpg)

![fig-35.jpg](figures/fig-35.jpg)

![fig-36.jpg](figures/fig-36.jpg)

![fig-37.jpg](figures/fig-37.jpg)

![fig-38.jpg](figures/fig-38.jpg)

![fig-39.jpg](figures/fig-39.jpg)

![fig-40.jpg](figures/fig-40.jpg)

