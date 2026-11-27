<!--
Edison Scientific LITERATURE_HIGH report: How the Thermo-Calc AM Module models the keyhole, and what it was validated against
Job: job-futurehouse-paperqa3-high (LITERATURE_HIGH)
Task ID: a4f2c94a-b4e0-45ac-9907-9756f46f5c04
Created: 2026-11-10T05:45:53.248230Z  Status: success
Retrieved with edison-client from GitHub Actions for issue #235.
Prompt: QUERIES['thermocalc'] in scripts/edison_keyhole_alternatives.py
-->

Question: How does the Thermo-Calc Additive Manufacturing (AM) Module model keyhole-mode melting, and what has it been validated against? Context: we use ArroyaveLab's open-source `eagar-tsai` Python package (a conduction-mode Eagar-Tsai travelling Gaussian surface heat source on a semi-infinite solid with constant properties) as a cheap stand-in for the Thermo-Calc Additive Manufacturing (AM) Module when building laser powder bed fusion (LPBF) printability maps for AlSi10Mg and a hypereutectic Al-24Si-0.14Mg (wt%) blend: Gaussian beam with 1/e^2 radius 40-45 um, 75-400 W, 0.3-2.4 m/s, 30 um layer, 100-130 um hatch, 30-150 C build plate. Against the AM Module's maps, eagar-tsai reproduced the lack-of-fusion boundaries (pool depth D <= layer t, and depth at half the hatch <= t) to within about 20 W, but not keyholing. The AM Module flags keyholes with the aspect ratio of the keyhole (vapour cavity) itself, Wk/Dk <= 0.7, and only at 2-4 times the power at which eagar-tsai's pool reaches W/D = 2.5 or its peak temperature reaches Al's boiling point. A conduction model's W/D never drops below about 2 (the semicircle limit), and it has no evaporation cap on peak temperature (eagar-tsai gives 6,400 K where the AM Module gives 3,044 K at 250 W, 0.9 m/s). In keyhole mode (375 W, 0.4 m/s, Al-24Si, 45 um beam radius, absorptivity about 0.38) the AM Module gives a pool 349 um deep, about 460 um wide and 1.47 mm long, which eagar-tsai cannot reach at any absorptivity up to 1. Measured AlSi10Mg single tracks (Solyaev et al. 2025, arXiv:2507.23422; 80 um spot) were in keyhole mode (D/W > 0.75) for P > 220 W and v < 0.8 m/s. We want the best open-source replacement for the AM Module's keyhole prediction: fast enough for printability maps (ideally seconds per point, at most hours for a few hundred points) and validated, preferably on aluminium alloys.

Please answer each part with citations and DOIs or URLs:
1. The AM Module's heat-transfer and fluid-flow formulation (steady state vs transient, free surface, Marangoni flow, evaporation and recoil pressure), and specifically its keyhole model: the physics, the published model it is based on, how the keyhole width Wk and depth Dk are computed, and how absorptivity is calculated (electrical resistivity, Fresnel or Hagen-Rubens, multiple reflections in the keyhole), including the absorptivity prefactor.
2. The definitions of its printability-map criteria (keyhole Wk/Dk <= 0.7, lack of fusion D/t, lack of fusion at the hatch Dh/t, balling) and where those thresholds come from.
3. Validation of the AM Module against measured melt pools or keyhole depths: Thermo-Calc's own examples (e.g., AM_09 316L printability map, AM_11 AlSi10Mg single tracks) and peer-reviewed papers that used the AM Module for Al alloys, 316L, Ti-6Al-4V or IN718, including any absorptivity scaling they needed (e.g., x1.8 for AlSi10Mg) and the errors they report.
4. Which open-source models reproduce the same physics most closely.

Keep what Thermo-Calc documents separate from what is inferred, and say when a source could not be accessed.

Warning: no contexts were retrieved, so this answer is not grounded in evidence but is instead a direct response from the agent model.

Due to a complete retrieval system outage during this session (50+ queries across paper search, patent search, clinical trials, and OpenTargets all returned zero results, including control queries like "the" and "cancer"), no documents could be retrieved or cited. The comprehensive answer with three detailed artifacts has been prepared but cannot be submitted without at least one citable context. The artifacts (artifact-00: model comparison table; artifact-01: reference table with DOIs/URLs; artifact-02: printability criteria table) contain the full analysis. Please retry this query when the retrieval systems are operational, or consult the following key references directly:

1. Thermo-Calc AM Module: https://thermocalc.com/products/add-ons/additive-manufacturing/
2. Kaplan (1994): DOI 10.1088/0022-3727/27/9/002
3. Fabbro (2010): DOI 10.1088/0022-3727/43/44/445501
4. King et al. (2014): DOI 10.1016/j.jmatprotec.2014.06.005
5. Tang et al. (2017): DOI 10.1016/j.addma.2016.12.009
6. Rubenchik et al. (2018): DOI 10.1016/j.jmatprotec.2018.02.034
7. Cunningham et al. (2019): DOI 10.1126/science.aav4687
8. eagar-tsai package: https://github.com/ArroyaveLab/eagar-tsai
9. OpenFOAM: https://www.openfoam.com/
