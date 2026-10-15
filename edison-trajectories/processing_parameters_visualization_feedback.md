# Processing Parameters Visualization Feedback

*Edison Scientific ANALYSIS feedback — 7 iterations across tile grid replacement*

## Iteration History (Sunburst → Tile Grid)

### Cycles 1–2: Original Sunburst (superseded)
- Cycle 1 (task `ee2c55b7`, 7 citations): Single color encoding, panel labels, argumentative title
- Cycle 2 (task `4ef7c34a`, 5 citations): Verified cycle 1 changes; cross-panel semantics

### Cycle 3: Tile Grid Introduction (task `f829d8b8`)
- Validated tile grid as "strong conceptual replacement" per Cleveland & McGill 1984
- Identified font sizing and WCAG contrast issues

### Cycle 4: Accent-Border Encoding (task `397a413b`) — 5.5/10
- Recommended accent-border encoding (light tile body + colored left bar)
- WCAG AA ≥7:1 contrast target for text on tiles

### Cycle 5: Print-Scale Fixes (task `a1dd5e67`) — 6.5/10
- Top 5 fixes: tile label fonts ≥7pt at print, accent bars 2× wider, red/gold hue separation, consistent gutters, stronger row bands
- Red (#C92A2A) replaces vermilion (#D55E00) for >3:1 separation from gold
- Gray accent bars (#5C6B77) with outline for "Typically fixed" visibility

### Cycle 6: Layout Issues (task `4820059d`) — 6.0/10
- Found text collisions at Panel B/C boundary (BO callout over subtitle)
- Tile overflow/clipping on 8-parameter rows
- Recommended 9–10pt tile labels for 6pt print floor

### Cycle 7: Layout Restructure (task `c22c3239`) — 5.5/10
- Panel A in side column was catastrophically cramped
- Recommended: Panel A full-width on top, B/C side-by-side below
- Score dropped because fonts expanded but layout didn't accommodate them

### Cycle 8: Refined Layout (task `7c9843e2`) — 7/10
- "A-on-top layout: Clear improvement"
- Shortened category headers prevent truncation
- Separated legends (category → upper right, status → bottom)
- Enlarged Panel C nodes for readability

### Cycle 9: Final Polish (task `503e6530`) — 8/10
- "Strong, near-publication-quality figure with compelling narrative arc"
- Final 3 fixes: subtitle collision, "36" badge overlap, legend/axis padding
- "Fixing these three issues would bring it to 9/10"

## Key Scientific Points from Edison (supported by citations)
- VED is widely used but fails as a complete descriptor: many parameter sets map to the same VED while producing different outcomes (Ferro et al. 2020, 142 cit.; Caiazzo et al. 2020, 113 cit.; Zavala-Arredondo et al. 2019, 77 cit.)
- Spears and Gold listed ~50 key LPBF parameters (Buhairi et al. 2023, 204 cit.)
- BO has been applied to LPBF parameter selection and in-situ tuning (Chepiga et al. 2023, 29 cit.; Kavas et al. 2025, 18 cit.)
- Multi-material LPBF requires material-specific parameter studies (Schanz et al. 2022, 14 cit.)
- Tile grids outperform sunbursts for countable taxonomies (Cleveland & McGill 1984)

## References (from Edison feedback cycles)

### Cycles 1–2 References
1. Buhairi et al. 2023. "Review on volumetric energy density: influence on morphology and mechanical properties of Ti6Al4V manufactured via LPBF." Progress in Additive Manufacturing, 8:265-283. doi:10.1007/s40964-022-00328-0. 204 citations.
2. Baghi et al. 2023. "A new approach to empirical optimization of LPBF process for Ti6Al4V parts." JMEP, 32:9472-9488. doi:10.1007/s11665-023-08060-8. 16 citations.
3. Zavala-Arredondo et al. 2019. "Use of power factor and specific point energy as design parameters in L-PBF of AlSi10Mg alloy." Materials & Design, 182:108018. doi:10.1016/j.matdes.2019.108018. 77 citations.
4. McCarthy 2025. "Surrogate-based multi-objective optimization of modulated wave LPBF using active learning." (preprint)
5. Schanz et al. 2022. "Individual process development of single and multi-material laser melting in novel modular LPBF system." Progress in Additive Manufacturing, 7:481-493. doi:10.1007/s40964-022-00276-9. 14 citations.
6. Ferro et al. 2020. "A modified volumetric energy density–based approach for porosity assessment in AM process design." IJAMT, 110:1911-1921. doi:10.1007/s00170-020-05949-9. 142 citations.
7. Caiazzo et al. 2020. "On the relevance of volumetric energy density in the investigation of Inconel 718 LPBF." Materials, 13:538. doi:10.3390/ma13030538. 113 citations.

### Cycle 2 References
8. Badini et al. 2024. "Laser powder bed fusion of pure titanium: optimization of processing parameters by means of efficient VED approach." Metals, 14:1357. doi:10.3390/met14121357. 6 citations.
9. Chepiga et al. 2023. "Process parameter selection for production of stainless steel 316L using efficient multi-objective Bayesian optimization algorithm." Materials, 16:1050. doi:10.3390/ma16031050. 29 citations.
10. Kavas et al. 2025. "In-situ controller autotuning by Bayesian optimization for closed-loop feedback control of LPBF process." arXiv. doi:10.48550/arxiv.2406.19096. 18 citations.

## Process-block draft feedback (new account / Edison API)

### Cycle 15: Process-representative blocks (task `c021f80a-212e-4d5f-8950-98c2f47d3c7a`) — 6.5/10
- Submitted through the official `edison-client` v0.12.0 API. Official docs show `EdisonClient(api_key=...)` and the installed client resolves `Stage.PROD` to `https://api.platform.edisonscientific.com`; `api.edisonscientific.com` did not resolve from the sandbox.
- Edison assessment: the generic-cube objection is substantially addressed; six of seven blocks carry recognizable LPBF cues.
- Required fixes:
  - Replace parameter-chip layout with a flexible packer to prevent overlap at proposal scale.
  - Fix missing Powder/Feedstock `reuse` chip.
  - Redraw Layer/Build: tilted layer stack and tree-support silhouette instead of X-zigzags.
  - Move Powder/Feedstock moisture cue into the powder bed as a labeled particle (`H₂O`).
- High-value polish applied:
  - Scan Strategy rotation arc anchored to a pivot dot and bidirectional hatch arrows added.
  - Atmosphere chamber now includes a tiny build plate + part silhouette.
  - Machine-Specific arrows unified; powder dosing shown as dotted arrow with micro-legend.
  - Thermal Mgmt clock labeled as inter-layer dwell and rotated/clipped text removed.
  - v6 composite tightened vertically.
