<!-- Extracted from Edison tokenization of adma70703-sup-0001-suppmat.pdf -->

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
