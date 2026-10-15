Materials criticality
2. Assessing raw materials criticality
Sterling G Baird and Taylor D Sparks
Materials Science & Engineering Department, University of Utah, Salt Lake City, UT, 84112, United States of America

Status
Raw materials criticality can significantly impact global markets [1]. For example, the historical cobalt crisis of 1977–1979 consisted of a violent rebellion in Zaire (0.009% global GDP at the time) that led to a price spike by 380% [1]. In 2011, China implemented export quotas and taxes on rare earth materials, increasing the price of permanent magnet Dy and Nd materials up by approximately 800% and 2050%, respectively, which took several years to resolve via a World Trade Organization trade dispute [2]. Both cobalt and rare-earth materials, along with many other elements, are foundational for renewable or low-carbon technology, and the dependence of low-carbon technologies (e.g. solar, wind, batteries) on critical materials affects the energy security of nations [3]. There is a growing shift towards alternative, sustainable renewable energy [2], battery [2, 4], thermoelectric [5], piezoelectric, ferroelectric, and drilling/cutting/grinding (e.g. automotive, oil, and gas) [6] technologies. Clearly, energy materials are heavily impacted; however, all materials and related applications will be affected by materials criticality. Therefore, for all materials, it is important to consider raw materials criticality questions such as:

Is a particular element abundant or scarce? (Elemental scarcity).
Is it sourced primarily from a single region? (Market concentration).
Do the region(s) suffer from political instability or frequent, disruptive, natural disasters? (Supply disruption risk).
How much can secondary sources relieve the above constraints? (Substitutes [7], recycling [2], see figure 1).
How do the above factors depend on the short-, medium-, and long-term? (Temporal [7, 8]).

Zoom InZoom OutReset image size
Figure 1. A flow analysis for materials criticality considerations demonstrates the dependence of materials criticality on and interdependence of many diverse factors, labelled as rates and displayed as gauges. Materials flow from resource base to resources and reserves, moving through manufacturing, recycling, consumption and in-use phases with circulatory connections in-between. Reprinted with permission from [1]. Copyright (2007) American Chemical Society.

Download figure:

Standard imageHigh-resolution image
Specifically, raw material criticality is a function of geographic, geological, environmental, political, temporal, and economic factors and is difficult to quantify (figure 1). Advancing understanding of the impact of raw materials criticality on industries for businesses, education, and governments [7] and increasing global data/analysis accessibility will enable:

More efficient use of natural, monetary, and temporal resources;
Avoidance of future supply-chain disruptions;
Acceleration of materials discovery for game-changing technologies.

For a detailed report of materials criticality provided by the US Department of Energy (DoE), see [7].

Current and future challenges
Raw materials criticality needs to be assessed quantitatively in addition to qualitative measures so that data can be incorporated into algorithms to identify existing, high-risk materials as well as sustainable, alternative candidates. We present this in three distinct, data-driven components:

(a)  
Identification and selection of meaningful features/metrics;
(b)  
Data curation and sanitation;
(c)  
Data analysis, interpretation, and visualisation.

Identification and selection of meaningful features/metrics
As a highlight of the ambiguity involved with defining ‘raw materials criticality’, Schellens and Gisladottir [9] gave a list of 23 distinct definitions across various review articles and gave a suggestion for a holistic definition. Alonso et al [1] identified 14 raw materials criticality features/metrics from 12 articles and sorted these into two categories: (a) institutional inefficiencies that cause resource unavailability and (b) physical constraints on amount and quality of resources. When a resource lacks certain institutional efficiencies, such as geographical supply and demand diversity or established recycling practices, the market is more susceptible to unpredictable events such as political change and natural disasters. Physical constraints were further sorted into static Malthusian (total amount and current rate of consumption), dynamic Malthusian (total amount and expected rates of consumption), and Ricardian (material quantity and quality) features, demonstrating the diversity of features that can exist. They also showed a material flow analysis (figure 1) which highlighted dependence on and interdependence of many, diverse factors. Some features may exhibit higher importance based on the application (as determined by feature selection algorithms), yet feature selection approaches may benefit from considering ease of obtaining and availability [10] of data in addition to importance.

Data curation and sanitation
Data may be subject to large uncertainty [1, 10], gaps [5], or systemic bias, any of which can depend on both material and temporal factors. For example, some materials (e.g. Li, Ni, Ga) are studied much more frequently than others (e.g. Cs, Tl, and Th) [8] and some material data has higher uncertainty (e.g. Herfindahl–Hirschman index (HHI) of Ga, Hf, Os) [5] or is missing data for certain years [5].

Data analysis, interpretation, and visualisation
Once data has been obtained and curated, screening can take the form of thresholds [1] and multi-objective optimisation for an application of interest [4–6]. Analysis and interpretation can be accomplished via machine learning algorithms or visual analysis of high-information density charts and tables. Algorithms or analyses which cater to input uncertainty or handle cases of sparse or missing data may be particularly useful.

Advances in science and technology to meet challenges
Hayes and McCullough [8] introduced a ‘percent criticality’ metric which they defined as the number of times an element was identified as critical vs the number of times an element was considered based on 32 comprehensive raw materials criticality studies. They analysed geographical, by-product recovery, and temporal trends using per cent criticality and found that rare earth elements, platinum-group metals, In, W, Ge, Co, Nb, Ta, Ga, Sb, Bi, Tl, and Mg are commonly considered critical.

The DoE’s 2011 materials criticality document [7] identified Dy, Tb, Eu, Nd, and Y as near-term high criticality energy materials. They assigned qualitative measures of a material’s importance to clean energy and supply risk (rankings between 1 and 4) and visualised these in gridded, criticality matrices for short- and medium-term forecasts.

Successful examples of identifying new, promising materials have been demonstrated in the search of new, sustainable thermoelectric [5], battery [4], and superhard [6] materials using data compiled from the CRC Handbook of Chemistry and Physics and United States Geological Survey commodity statistics for elemental scarcity and the HHI, respectively (figure 2).

Zoom InZoom OutReset image size
Figure 2. Elemental abundance and scarcity ξ (lower triangles), HHI production (left quadrilaterals) and HHI reserve (right quadrilaterals) data used for sustainable materials discovery is overlaid on the periodic table of elements. Unavailable data is portrayed as white. Reprinted with permission from [5]. Copyright (2013) American Chemical Society.

Download figure:

Standard imageHigh-resolution image
Gaultois et al [5] demonstrated that Te often correlates with high performance in thermoelectrics but has high scarcity. Despite being rare, the HHI value (a measure of market concentration) is low (good). In other words, the market is non-concentrated and less susceptible to local fluctuation.

Ghadbeigi et al [4] revealed that high energy battery materials (more typical of layered crystal structures) are scarcer than high power battery materials (more typical of olivine and spinel structures). They also showed that FeS2 can deliver good specific energy while having high abundance, and that Sb has more sustainable alternatives such as Si, Mn, Ni, Cu, and/or Zn.

Mansouri Tehrani et al [6] screened 1100 compounds for hardness values above 20 GPa and plotted the remainder in a high-information density plot (figure 5 of [6]). The abscissa (x-axis), ordinate (y-axis), colour, and plot marker size represented production HHI, scarcity, synthesis type (high-temperature/high-pressure vs high-temperature-only), and experimental hardness value (higher value = larger marker), respectively. By visually inspection, they identified best choices (diamond, c-BC5, c-BN, and BC2N), lower hardness alternatives (TiC, SiC, and TaB2), and poor choices (market-concentrated WB4 and transition metal candidates containing non-abundant Re, Ru, and Os).

Concluding remarks
Raw materials criticality is an important consideration for material selection. However, identifying and selecting criticality metrics, obtaining and curating data, and analysing and interpreting it can present significant challenges in the form of lack of availability, inconsistent reporting, and difficult to predict events (e.g. political uncertainty and natural disasters). Materials discovery approaches that incorporate criticality metrics have been successful in identifying new and sustainable thermoelectric, battery, and superhard materials. Improvements in raw materials criticality data availability and accessibility and increased use of criticality data in material informatics can enable more efficient use of resources, better supply-chain stability, and accelerated materials discovery for future technologies.

Acknowledgments
T D S and S G B gratefully acknowledge support from the National Science Foundation (CMMI-1562226 and DMR-1651668).