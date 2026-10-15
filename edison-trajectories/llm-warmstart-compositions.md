# LLM-Suggested Al-Si-Mg Compositions for BOFN Warmstarting

*Edison Scientific LITERATURE query (task 16953cd8)*

Question: I am performing Bayesian optimization over a function network for alloy discovery 
in a ternary Al-Si-Mg system. The pipeline has 4 stages: CALPHAD thermodynamic screening, 
powder atomization, laser powder bed fusion (LPBF) printing, and mechanical characterization.

The CALPHAD screening node takes 3 composition inputs (weight fractions of Al, Si, Mg that sum to 1.0) 
and predicts phase stability (higher = better). Desirable compositions have good phase stability, 
narrow solidification range, and are amenable to LPBF processing.

Please suggest 15 specific ternary Al-Si-Mg compositions (as weight fractions summing to 1.0) 
that would be good starting points for LPBF alloy optimization. For each composition, give:
1. The three weight fractions (Al, Si, Mg) 
2. A brief rationale (1 sentence)

Format each composition as: Al=X.XX, Si=Y.YY, Mg=Z.ZZ

Include a mix of:
- Well-known LPBF-printable compositions (e.g., AlSi10Mg variants)
- Compositions near solidification minima
- A few exploratory compositions outside the typical range

Focus on compositions where Al is the majority component (>60 wt%).

The candidate starting points below are Al-rich ternary Al–Si–Mg weight-fraction compositions (each sums to 1.00, Al>0.60) chosen to (i) include widely used LPBF powders (AlSi10Mg and AlSi7Mg-type ranges), (ii) sample near-eutectic Si where freezing range and LPBF solidification cracking susceptibility are minimized, and (iii) add a few exploratory higher-Si and higher-Mg perturbations to help Bayesian optimization map phase-stability/printability tradeoffs before downselecting via CALPHAD screening (hyer2021compositiondependentsolidificationcracking pages 1-2, cauwenbergh2018heattreatmentoptimization pages 1-2, hyer2021compositiondependentsolidificationcracking pages 4-5).

| # | Composition | Rationale |
|---|---|---|
| 1 | Al=0.90, Si=0.10, Mg=0.00 | Baseline near the classic AlSi10 family, useful for isolating the effect of Mg in later CALPHAD and LPBF screening around a well-known printable Si level (hyer2021compositiondependentsolidificationcracking pages 1-2, cauwenbergh2018heattreatmentoptimization pages 1-2). |
| 2 | Al=0.90, Si=0.10, Mg=0.01 | A direct AlSi10Mg-type starting point matching literature that reports Al-10Si-0.5Mg as crack-free in LPBF and explores Mg-enabled strengthening via Mg2Si (hyer2021compositiondependentsolidificationcracking pages 1-2, gandolfi2021relationshipbetweenmicrostructure pages 2-3). |
| 3 | Al=0.89, Si=0.10, Mg=0.01 | This slightly Mg-richer AlSi10Mg variant probes the upper end of the explored 1 wt% Mg space while staying close to a familiar printable Si content (gandolfi2021relationshipbetweenmicrostructure pages 2-3, gandolfi2021relationshipbetweenmicrostructure pages 1-2). |
| 4 | Al=0.90, Si=0.09, Mg=0.01 | A slightly hypoeutectic AlSi9Mg1 candidate tests whether marginally lower Si retains LPBF processability while benefiting from stronger Mg2Si-forming potential (gandolfi2021relationshipbetweenmicrostructure pages 2-3, gandolfi2021relationshipbetweenmicrostructure pages 1-2). |
| 5 | Al=0.91, Si=0.08, Mg=0.01 | This exploratory AlSi8Mg1 composition moves toward lower Si but still within a region where increasing Si is known to improve freezing behavior, making it a useful boundary point for screening (pataric2025theroleof pages 6-9, pataric2025theroleof pages 1-3). |
| 6 | Al=0.92, Si=0.07, Mg=0.01 | This AlSi7Mg1-style point is anchored to the common AlSi7Mg window and adds a higher-Mg perturbation to test strengthening against any thermodynamic penalties (cauwenbergh2018heattreatmentoptimization pages 1-2, gandolfi2021relationshipbetweenmicrostructure pages 1-2). |
| 7 | Al=0.92, Si=0.07, Mg=0.01 | A representative AlSi7Mg composition aligned with commercial LPBF powder ranges, making it a practical lower-Si benchmark for the network (cauwenbergh2018heattreatmentoptimization pages 1-2). |
| 8 | Al=0.91, Si=0.08, Mg=0.00 | This A356-like low-Mg variant sits between AlSi7Mg and AlSi10Mg and can help map how Si-driven narrowing of freezing range begins before the near-eutectic regime (pataric2025theroleof pages 6-9, cauwenbergh2018heattreatmentoptimization pages 1-2). |
| 9 | Al=0.89, Si=0.11, Mg=0.00 | Near the upper commercial AlSi10Mg Si range, this composition is a practical printability-focused starting point before moving fully toward eutectic Si levels (cauwenbergh2018heattreatmentoptimization pages 1-2, qin2020rapidsolidificationand pages 1-2). |
| 10 | Al=0.88, Si=0.12, Mg=0.00 | This near-eutectic composition targets the well-established LPBF-friendly high-Si region where freezing range is reduced and cracking tendency drops (hyer2021compositiondependentsolidificationcracking pages 1-2, hyer2021compositiondependentsolidificationcracking pages 4-5). |
| 11 | Al=0.87, Si=0.12, Mg=0.01 | Adding 1 wt% Mg to a near-eutectic Si level tests whether good solidification behavior can be combined with more Mg2Si-based strengthening potential (hyer2021compositiondependentsolidificationcracking pages 1-2, gandolfi2021relationshipbetweenmicrostructure pages 2-3). |
| 12 | Al=0.86, Si=0.13, Mg=0.01 | This composition sits very close to the reported ~12.6 wt% Si eutectic neighborhood while adding Mg for precipitation hardening, making it a strong candidate for CALPHAD triage (hyer2021compositiondependentsolidificationcracking pages 1-2, gandolfi2021relationshipbetweenmicrostructure pages 2-3). |
| 13 | Al=0.85, Si=0.14, Mg=0.01 | A modestly hypereutectic-leaning exploratory point extends into the crack-free high-Si LPBF window while preserving Al as the majority constituent (hyer2021compositiondependentsolidificationcracking pages 4-5). |
| 14 | Al=0.84, Si=0.15, Mg=0.01 | This higher-Si exploratory candidate probes the upper end of the LPBF-tolerant Si range reported in Al-Si studies, with Mg included to evaluate ternary eutectic/strengthening tradeoffs (hyer2021compositiondependentsolidificationcracking pages 4-5, gandolfi2021relationshipbetweenmicrostructure pages 1-2). |
| 15 | Al=0.83, Si=0.16, Mg=0.01 | This deliberately high-Si exploratory point samples the reported crack-free 16 wt% Si neighborhood and can test whether CALPHAD predicts acceptable phase stability and LPBF amenability despite the larger eutectic fraction (hyer2021compositiondependentsolidificationcracking pages 4-5). |


*Table: This table lists 15 suggested Al-rich ternary Al–Si–Mg starting compositions for LPBF alloy optimization, spanning known printable alloys, near-eutectic solidification-friendly candidates, and exploratory high-Mg/high-Si points. The rationales are tied to literature-based LPBF printability and solidification trends and are framed as inputs for subsequent CALPHAD screening.*

These suggestions are grounded in reports that Al–Si alloys near the eutectic (~12.6 wt% Si) can produce dense/crack-free LPBF parts (including Al–10Si–0.5Mg and higher-Si 12.6–16 wt% cases), and that increasing Si in hypoeutectic Al–Si–Mg narrows the freezing/feeding range; Mg is included in the typical commercial LPBF windows (and in a few higher-Mg variants) to enable precipitation hardening via Mg2Si while still keeping Al as the majority component (hyer2021compositiondependentsolidificationcracking pages 1-2, cauwenbergh2018heattreatmentoptimization pages 1-2, hyer2021compositiondependentsolidificationcracking pages 4-5, pataric2025theroleof pages 1-3).

References

1. (hyer2021compositiondependentsolidificationcracking pages 1-2): Holden Hyer, Le Zhou, Abhishek Mehta, Sharon Park, Thinh Huynh, Shutao Song, Yuanli Bai, Kyu Cho, Brandon McWilliams, and Yongho Sohn. Composition-dependent solidification cracking of aluminum-silicon alloys during laser powder bed fusion. Acta Materialia, 208:116698, Apr 2021. URL: https://doi.org/10.1016/j.actamat.2021.116698, doi:10.1016/j.actamat.2021.116698. This article has 225 citations and is from a highest quality peer-reviewed journal.

2. (cauwenbergh2018heattreatmentoptimization pages 1-2): P Van Cauwenbergh, A Beckers, and L Thijs. Heat treatment optimization via thermo-physical characterization of alsi7mg and alsi10mg manufactured by laser powder bed fusion (lpbf). Unknown journal, 2018.

3. (hyer2021compositiondependentsolidificationcracking pages 4-5): Holden Hyer, Le Zhou, Abhishek Mehta, Sharon Park, Thinh Huynh, Shutao Song, Yuanli Bai, Kyu Cho, Brandon McWilliams, and Yongho Sohn. Composition-dependent solidification cracking of aluminum-silicon alloys during laser powder bed fusion. Acta Materialia, 208:116698, Apr 2021. URL: https://doi.org/10.1016/j.actamat.2021.116698, doi:10.1016/j.actamat.2021.116698. This article has 225 citations and is from a highest quality peer-reviewed journal.

4. (gandolfi2021relationshipbetweenmicrostructure pages 2-3): Maressa Gandolfi, Marcella Gautê Cavalcante Xavier, Leonardo Fernandes Gomes, Rodrigo André Valenzuela Reyes, Amauri Garcia, and José Eduardo Spinelli. Relationship between microstructure evolution and tensile properties of alsi10mg alloys with varying mg content and solidification cooling rates. Metals, 11:1019, Jun 2021. URL: https://doi.org/10.3390/met11071019, doi:10.3390/met11071019. This article has 24 citations.

5. (gandolfi2021relationshipbetweenmicrostructure pages 1-2): Maressa Gandolfi, Marcella Gautê Cavalcante Xavier, Leonardo Fernandes Gomes, Rodrigo André Valenzuela Reyes, Amauri Garcia, and José Eduardo Spinelli. Relationship between microstructure evolution and tensile properties of alsi10mg alloys with varying mg content and solidification cooling rates. Metals, 11:1019, Jun 2021. URL: https://doi.org/10.3390/met11071019, doi:10.3390/met11071019. This article has 24 citations.

6. (pataric2025theroleof pages 6-9): Aleksandra Patarić, Mile Djurdjevic, Srecko Manasijevic, Srecko Stopic, and Marija Mihailović. The role of silicon during solidification process of cast al-si-mg alloys. Materials, 18:5033, Nov 2025. URL: https://doi.org/10.3390/ma18215033, doi:10.3390/ma18215033. This article has 2 citations.

7. (pataric2025theroleof pages 1-3): Aleksandra Patarić, Mile Djurdjevic, Srecko Manasijevic, Srecko Stopic, and Marija Mihailović. The role of silicon during solidification process of cast al-si-mg alloys. Materials, 18:5033, Nov 2025. URL: https://doi.org/10.3390/ma18215033, doi:10.3390/ma18215033. This article has 2 citations.

8. (qin2020rapidsolidificationand pages 1-2): Hong Qin, Qingshan Dong, Vahid Fallah, and Mark R. Daymond. Rapid solidification and non-equilibrium phase constitution in laser powder bed fusion (lpbf) of alsi10mg alloy: analysis of nano-precipitates, eutectic phases, and hardness evolution. Metallurgical and Materials Transactions A, 51:448-466, Nov 2020. URL: https://doi.org/10.1007/s11661-019-05505-5, doi:10.1007/s11661-019-05505-5. This article has 115 citations.