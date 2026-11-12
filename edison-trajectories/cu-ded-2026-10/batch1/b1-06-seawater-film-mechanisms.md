<!--
Edison Scientific LITERATURE task (batch 1)
- Task ID: 695a9d41-f20a-4d61-ae57-92af3b1248ee
- Submitted: 2026-10-17T05:10:45Z
- Fetched: 2026-10-17T05:42:07Z (status: success)
- Raw trajectory JSON: ../raw/b1-06-seawater-film-mechanisms.json.gz
- Synthesis: ../README.md
-->

Question:

CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Manufacturing Engineering, Brigham Young University; EXCLUDE the
PI's own publications) is writing an ONR FY2027 Young Investigator Program
proposal for the Materials & Processes for Additive Manufacturing program.
The work designs new pre-alloyed copper alloy powders for single-stream
blown-powder laser directed energy deposition (DED; one pre-alloyed powder
feed, not in-situ blending of elemental powders). Goals: deposits that are
dense and crack-free, both built on themselves and deposited on cast
nickel-aluminum bronze (NAB) and wrought Cu-Ni (repair), and that resist
seawater AS DEPOSITED (no post-build heat treatment) at least as well as
wrought 70-30 Cu-Ni (C71500). Alloy families: Cu-Ni (10-30 wt% Ni) with Fe,
Mn, Cr additions; aluminum bronzes / NAB with Ni, Fe, Mn. A secondary
objective is lower nickel content (nickel is a US critical mineral). Powder is
made in-house by ultrasonic atomization (AMAZEMET rePOWDER, induction
melting); size, Hall flow, apparent density and oxygen are measured per lot.
Method: the composition -> powder -> DED deposit -> microstructure ->
corrosion/hardness pipeline is a network of linked surrogate models searched
by cost-aware Bayesian optimization of function networks (cheap nodes such as
CALPHAD and short electrochemical tests are queried more often than expensive
ones such as 30-day immersion). ICME element: CALPHAD (Thermo-Calc) evaluated
along a heat-flow model of the DED thermal history, tested against
equilibrium-only CALPHAD and against no physics.

QUESTION: What controls the seawater corrosion resistance of Cu-Ni and
aluminum bronzes, and how does an as-solidified or as-deposited
microstructure change it? Cover protective film formation (Cu2O inner layer,
Ni/Fe-enriched outer layers, time to stabilize), the roles of Fe (1-2 wt%),
Mn and Cr, microsegregation and cored dendrites, kappa phases and martensite
in NAB (selective phase corrosion), velocity limits, sulfide-polluted water,
and biofouling. Which short electrochemical tests (polarization, LPR, EIS,
ASTM G59/G102/G106, G31 immersion) have been shown to rank copper alloys the
same way as long-term seawater exposure, and over what exposure time does
film formation make short tests misleading?

OUTPUT FORMAT: For each relevant item give the full citation with DOI, the
process (blown-powder laser DED / laser cladding / laser metal deposition,
wire-laser DED, wire-arc DED (WAAM), LPBF, cast, wrought), the alloy
composition in wt%, the test conditions (e.g. 3.5 wt% NaCl vs natural or
substitute seawater per ASTM D1141, duration, flow), and the key numbers
(porosity/density, corrosion current density or rate, Ecorr, impedance,
selective-attack depth, hardness, strength/elongation, powder size/flow/
oxygen). Tag each item: [CITE] worth citing; [NUMBERS] gives a quantitative
benchmark; [NAVY] Navy/DoD-funded or Navy application; [NOVELTY-RISK] overlaps
the proposed work (say how); [GAP] shows something not yet done. If the
literature does not answer part of the question, say so plainly instead of
padding with loosely related work. End with a ranked "Top 5 things the PI
should know" list.

---

Question: CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Manufacturing Engineering, Brigham Young University; EXCLUDE the
PI's own publications) is writing an ONR FY2027 Young Investigator Program
proposal for the Materials & Processes for Additive Manufacturing program.
The work designs new pre-alloyed copper alloy powders for single-stream
blown-powder laser directed energy deposition (DED; one pre-alloyed powder
feed, not in-situ blending of elemental powders). Goals: deposits that are
dense and crack-free, both built on themselves and deposited on cast
nickel-aluminum bronze (NAB) and wrought Cu-Ni (repair), and that resist
seawater AS DEPOSITED (no post-build heat treatment) at least as well as
wrought 70-30 Cu-Ni (C71500). Alloy families: Cu-Ni (10-30 wt% Ni) with Fe,
Mn, Cr additions; aluminum bronzes / NAB with Ni, Fe, Mn. A secondary
objective is lower nickel content (nickel is a US critical mineral). Powder is
made in-house by ultrasonic atomization (AMAZEMET rePOWDER, induction
melting); size, Hall flow, apparent density and oxygen are measured per lot.
Method: the composition -> powder -> DED deposit -> microstructure ->
corrosion/hardness pipeline is a network of linked surrogate models searched
by cost-aware Bayesian optimization of function networks (cheap nodes such as
CALPHAD and short electrochemical tests are queried more often than expensive
ones such as 30-day immersion). ICME element: CALPHAD (Thermo-Calc) evaluated
along a heat-flow model of the DED thermal history, tested against
equilibrium-only CALPHAD and against no physics.

QUESTION: What controls the seawater corrosion resistance of Cu-Ni and
aluminum bronzes, and how does an as-solidified or as-deposited
microstructure change it? Cover protective film formation (Cu2O inner layer,
Ni/Fe-enriched outer layers, time to stabilize), the roles of Fe (1-2 wt%),
Mn and Cr, microsegregation and cored dendrites, kappa phases and martensite
in NAB (selective phase corrosion), velocity limits, sulfide-polluted water,
and biofouling. Which short electrochemical tests (polarization, LPR, EIS,
ASTM G59/G102/G106, G31 immersion) have been shown to rank copper alloys the
same way as long-term seawater exposure, and over what exposure time does
film formation make short tests misleading?

OUTPUT FORMAT: For each relevant item give the full citation with DOI, the
process (blown-powder laser DED / laser cladding / laser metal deposition,
wire-laser DED, wire-arc DED (WAAM), LPBF, cast, wrought), the alloy
composition in wt%, the test conditions (e.g. 3.5 wt% NaCl vs natural or
substitute seawater per ASTM D1141, duration, flow), and the key numbers
(porosity/density, corrosion current density or rate, Ecorr, impedance,
selective-attack depth, hardness, strength/elongation, powder size/flow/
oxygen). Tag each item: [CITE] worth citing; [NUMBERS] gives a quantitative
benchmark; [NAVY] Navy/DoD-funded or Navy application; [NOVELTY-RISK] overlaps
the proposed work (say how); [GAP] shows something not yet done. If the
literature does not answer part of the question, say so plainly instead of
padding with loosely related work. End with a ranked "Top 5 things the PI
should know" list.


# Seawater corrosion of Cu–Ni and aluminum bronzes: implications for as-deposited DED

**Scope.** Compositions below are wt%; “not reported” means that the cited evidence does not establish the value. A corrosion current measured immediately after polishing is **not** an annual seawater penetration rate, and 3.5% NaCl is **not** natural seawater. No publication by Sterling G. Baird is included.

## Mechanisms and service conditions

**Cu–Ni films and alloying.** Marine-grade wrought 90/10 Cu–Ni, UNS C70600, typically contains Ni 9–11, Fe 1–2, Mn 0.5–1, balance Cu. Its protective corrosion-product film has a predominantly **Cu₂O inner component** and contains Ni-bearing species, iron oxides, copper hydroxychlorides and CuO in its more complex outer regions; it should not be treated as an instantaneous, stainless-steel-like passive film. The first film develops over days, but maturation in temperate seawater takes approximately **2–3 months**; corrosion rates can continue falling for **years**. A 14-year seawater exposure reported a rate approaching **1.3 µm/year after 5–6 years**, versus the broader anticipated service range **1–20 µm/year**. Ni and Fe enrichment are consequential film characteristics, not evidence that adding either element invariably improves every flow and stagnation condition. **[CITE] [NUMBERS] [NAVY]** Powell, C., “Corrosion and Biofouling Resistance Evaluation of 90-10 Copper-Nickel” (2004), Copper Development Association/Nickel Institute review; **DOI not identified**. (powell2004corrosionandbiofouling pages 1-4)

**Fe, Mn, Cr and dendrite chemistry.** Approximately 1–2% Fe and modest Mn additions improve Cu–Ni impingement/erosion–corrosion resistance **when Fe remains adequately distributed**. Segregated Fe can instead encourage localized corrosion; higher Fe is not automatically beneficial. Small Cr additions can substantially raise flow tolerance but Cr segregation may worsen quiet-water localized attack. These are reasons to measure **core-to-interdendrite Fe/Mn/Cr distributions**, rather than relying on nominal CALPHAD composition or hardness. Phull and Abdullahi report suggested maximum *heat-exchanger design* velocities of **3.0 m/s for C70600** and **3.7 m/s for C71500**; separately measured critical velocities were **4.5 m/s at 27°C for C70600**, **4.1 m/s at 12°C for C71500**, and **12 m/s at 27°C for Cr-modified C72200**. These different-temperature, geometry-dependent figures are **not** interchangeable operating guarantees. **[CITE] [NUMBERS] [GAP]** Phull, B., and Abdullahi, A. A., “2.18—Marine Corrosion,” *Comprehensive Materials Finishing* **2** (2017): 1107–1148, DOI **10.1016/B978-0-444-52787-5.00046-9**; processes: conventional copper-alloy tubing and seawater components; seawater flow tests and field experience. (phull20172.18–marine pages 25-27, phull20172.18–marine pages 27-28)

**Pollution and biology change the objective.** Sulfide from polluted intake water, sediment or sulfate-reducing bacteria (SRB) during stagnation interferes especially with *initial* Cu–Ni film formation. Reported tests spanning **7–250 ppb sulfide** found increasing attack; **1,000 ppb for 1–5 days**, or **10 ppb for 30 days**, could leave continued attack after clean-water flushing. Several months of clean-water prefilming can make brief later sulfide exposure less damaging. Copper alloys discourage, but do not eliminate, macrofouling; stagnant areas, deposits and dead organisms can foster under-deposit corrosion, while obstructions generate local impingement. Cathodic protection or galvanic coupling can also alter antifouling behavior. Thus clean, flowing, aerated NaCl alone is insufficient to establish naval performance. **[CITE] [NUMBERS] [NAVY]** Phull and Abdullahi (2017), DOI **10.1016/B978-0-444-52787-5.00046-9**; Powell (2004), **DOI not identified**. (phull20172.18–marine pages 25-27, phull20172.18–marine pages 27-28, powell2004corrosionandbiofouling pages 1-4)

**As-solidified NAB is a phase-selection problem.** The Cu-rich α matrix may contain Fe-rich κI/κII/κIV, Ni–Al-rich lamellar κIII, retained β′ martensite, or undesirable Al-rich γ₂. Ni and Fe suppress γ₂ by changing Al partitioning, but increasing Ni is not unconditionally required: the **fraction, continuity, chemistry and spacing** of β′ and κ phases determine microgalvanic/selective attack. Preferential corrosion may involve β′ itself, κIII itself, *or α adjacent to κ*, depending on microstructure and environment; these observations should not be conflated. Repeated DED thermal cycles can transform phases differently at the top layer, remelt bands, heat-affected substrate and repair interface. **[CITE] [GAP]** Fayanas, A., Veiga, A., Perez, A., Concustell, A., Molas, S., and Ordas, N., “Nickel Aluminium Bronze Alloys with Enhanced Erosion-Corrosion Resistance and Mechanical Strength,” *Journal of the Japan Society of Powder and Powder Metallurgy* **72** (2025): S819–S826, DOI **10.2497/jjspm.15F-T13-08**; and Nemani et al., cited below. (fayanas2025nickelaluminiumbronze pages 1-2, nemani2024advancementsinadditive pages 62-68, nemani2024advancementsinadditive pages 79-83)

## Quantitative studies and closest prior art

1. **Time-resolved C71500 benchmark—wrought Cu–Ni.** Al-Muhanna, K., and Habib, K., “Corrosion behavior of different alloys exposed to continuous flowing seawater by electrochemical impedance spectroscopy (EIS),” *Desalination* **250** (2010): 404–407, DOI **10.1016/j.desal.2009.09.065**. **Process:** conventional Cu–Ni 70/30, reported Cu 69/Ni 30/Fe 0.5/Mn 0.5, compared with 304 stainless steel, Hastelloy G-30 and Ti. **Conditions:** continuously renewed natural Kuwait Gulf seawater, **180 days**, water **18–33°C**; flow velocity not reported in the extracted text; EIS at 0, 1, 5, 20 and 30 days and monthly thereafter. For Cu–Ni, area-normalized EIS resistance changed from **6.933 kΩ·cm² initially** to **18.63 at day 1**, **81 at day 20**, **26.4 at day 30**, and **40.3 at day 180**; reported EIS-derived current was **3.75, 15, 0.32, 0.98 and 0.65 µA/cm²**, respectively. Biological/seasonal effects complicated trends. These are **same-specimen longitudinal estimates**, **not** proof that an early EIS ranking predicts six-month mass loss. **[CITE] [NUMBERS] [NAVY]** (almuhanna2010corrosionbehaviorof pages 1-2, almuhanna2010corrosionbehaviorof pages 2-4)

2. **A useful negative screening-control experiment—cast NAB.** Rivero, P. J., Berlanga, C., Palacio, J. F., and Biezma-Moraleda, M. V., “Effect of Ti on Microstructure, Mechanical Properties and Corrosion Behavior of a Nickel-Aluminum Bronze Alloy,” *Materials Research* **24** (2021), DOI **10.1590/1980-5373-MR-2020-0335**. **Process/composition:** sand-cast Cu 79.8/Al 9.5/Fe 4.8/Ni 4.6/Mn 1.3, versus the same nominal base alloy plus **120 ppm Ti**. **Conditions:** fresh Tafel/LPR in **3.5 wt% NaCl**, Ag/AgCl reference, and separate **720-hour**, room-temperature, still-NaCl immersion. Ti-free/Ti-added respectively: **gravimetric loss 0.034%/0.020%**, but electrochemically calculated rates **0.021/0.023 mm/year** and polarization resistances **2.4 × 10⁵/2.1 × 10⁵ Ω·cm²**; OCP **−150/−148 mV**. Hardness **172.46 ± 23.5/206.89 ± 20.2 HV**. The apparent *rank reverses* between weight loss and electrochemical rate, although the authors found **no statistically significant corrosion difference**. This is **not** a validated difference in long-term seawater resistance. **[CITE] [NUMBERS] [GAP]** (rivero2021effectofti pages 2-3, rivero2021effectofti pages 5-6, rivero2021effectofti pages 6-8, rivero2021effectofti pages 1-2)

3. **Film formation changes rankings within 20 days—cast versus powder-metallurgy NAB.** Fayanas et al. (2025), DOI **10.2497/jjspm.15F-T13-08**. **Processes/compositions:** continuous-cast Cu–9.7Al–4.4Ni–4.3Fe–0.9Mn; sinter+HIP Cu–10Al–5Ni–4Fe–1Mn; **not DED**. HIP-product relative density **99.2%**; a second, canister-HIP product reached **99.9%**, but was excluded from the corrosion comparison because of inadequate mechanical properties. **Conditions:** still **3.5 wt% NaCl**, room temperature; **20-minute OCP** followed by polarization at **1 mV/s**, tested fresh and after **480 hours** immersion; separate **48-hour**, **3.8 m/s**, 3%-sand slurry erosion–corrosion. Fresh cast versus sinter+HIP: **E_corr −0.260/−0.388 V**, **j_corr 9.90/6.85 µA/cm²**; after 480 hours: **−0.208/−0.277 V** and **6.45/3.02 µA/cm²**. Annealing changed results again: after 480 hours, heat-treated cast **2.12 µA/cm²** versus heat-treated sinter+HIP **10.4 µA/cm²**. As-processed cast versus sinter+HIP strengths were **773 ± 4/700 ± 9 MPa**, elongations **16.7 ± 1.2/15.6 ± 0.8%**, hardness **200 ± 1/190 ± 3 HV10**. Slurry losses were **8.7 versus 7.6 mg/cm²**. Cross sections reveal localized attack despite small differences in bulk electrochemical estimates; the paper’s Figure 11 directly illustrates why pit/phase mapping must accompany polarization. **[CITE] [NUMBERS] [GAP]** (fayanas2025nickelaluminiumbronze pages 1-2, fayanas2025nickelaluminiumbronze pages 2-5, fayanas2025nickelaluminiumbronze pages 5-7, fayanas2025nickelaluminiumbronze media 84062957)

4. **Months-long seawater can uncover deep selective corrosion missed by short tests.** Dobson, T., Larrosa, N., Reid, M., Rajamudili, K., Ganguly, S., and Coules, H., “Corrosion mechanisms of plasma welded nickel aluminium bronze immersed in seawater,” *Corrosion Science* (2024), DOI **10.1016/j.corsci.2024.112004**; numerical details checked against Dobson’s associated 2024 thesis, *Corrosion Mechanisms and Fatigue Behaviour of Marine Biofouled Plasma Welded Nickel Aluminium Bronze* (**thesis DOI not identified**). **Process:** plasma-welded cast NAB, parent **Cu balance/Al 9.14/Fe 4.38/Ni 4.84/Mn 0.09**. **Conditions:** natural seawater at approximately **1 m depth** in Plymouth marina for **12 or 18 months**, contrasted with simulated-seawater controls; naturally occurring biofouling and SRB, no controlled flow velocity. β′ near the weld preferentially corroded, changing toward κIII selective attack away from it; maximum measured κIII attack path **1,331 µm at 12 months**, and deepest pit under biofouling **986 µm** (mean **241 µm**, n=155). Natural seawater exhibited a different dominant dissolution pattern from simulated seawater. These are **maximum local depths**, emphatically not uniform mm/year rates. **[CITE] [NUMBERS] [NAVY]** (dobson2024corrosionmechanismsand pages 240-244, dobson2024corrosionmechanismsand pages 143-147, dobson2024corrosionmechanismsand pages 92-95, dobson2024corrosionmechanismsand pages 151-154)

5. **Direct novelty warning: prealloyed powder laser cladding onto like-composition cast bronze already exists.** Ziqiang, P., Kaiping, D., Xing, C., Zhaoran, Z., and Chen, W., “Laser cladding remanufacturing of propeller ZCuAl8Mn13Fe3Ni2 alloy,” *Scientific Reports* **15** (2025), DOI **10.1038/s41598-025-96674-4**. **Process/feedstock:** laser cladding using **gas-atomized prealloyed 45–150 µm powder**, deposited on the corresponding cast propeller bronze; powder Cu balance/Al **8.15**/Mn **13.16**/Fe **3.03**/Ni **2.11**. **Conditions:** optimized **1,600 W, 6 mm/s**; artificial seawater is mentioned for immersion, but the retrieved electrochemical exposure duration and flow are not established. Cladding hardness **278 HB**, **14.88% above cast**, but its polarization indicated **18.68% higher corrosion current** and **E_corr −0.271 V versus cast −0.266 V**. **Important source discrepancy:** the publication variously prints cladding current as **3.73 × 10⁻²** and **3.73 × 10⁻³ mA/cm²**; do **not** use the absolute current without checking the original curves/table. Powder Hall flow, apparent density, oxygen, deposit porosity and long-term comparative corrosion were not established in the retrieved evidence. This overlaps the proposed *single-prealloy-powder, laser-deposited bronze-on-cast-bronze repair*; novelty must be in systematic composition search, demonstrated as-deposited seawater durability and joint qualification, **not** merely the process combination. **[CITE] [NUMBERS] [NAVY] [NOVELTY-RISK] [GAP]** (ziqiang2025lasercladdingremanufacturing pages 1-3, ziqiang2025lasercladdingremanufacturing pages 6-9)

6. **As-built NAB is not inevitably worse than cast NAB.** Murray and coauthors, “Selective laser melting of nickel aluminium bronze,” *Additive Manufacturing* **33** (2020): 101122, DOI **10.1016/j.addma.2020.101122**. **Process:** **LPBF, not blown-powder DED**, using Cu balance/Al **9.8**/Ni **5.2**/Fe **4.6**/Mn **0.3** powder; powder-size/oxygen data not established here. The as-built condition was approximately uniform martensite without conventional κ precipitates; **600–700°C for 1 h** generated α+κ and improved its brittle tensile response. In reported **three- and six-month seawater mass-loss tests**, the *as-built* sample lost roughly **one order of magnitude less mass** than cast or wrought α+κ comparators. Absolute losses, natural-versus-substitute seawater classification and flow were not recovered, so the magnitude should be checked in the primary article before using it as a performance specification. The lesson is to test actual as-deposited phases: retained martensite may be locally susceptible in welded HAZs yet uniform martensitic LPBF material can avoid α/κ microgalvanic attack. **[CITE] [NUMBERS] [NOVELTY-RISK]** (camilleri2025coldsprayas pages 12-13, nemani2024advancementsinadditive pages 71-74, nemani2024advancementsinadditive pages 74-79)

7. **Laser-powder DED repair and strength precedents.** Nemani, A. V., Ghaffari, M., Bokati, K. S., Valizade, N., Afshari, E., and Nasiri, A., “Advancements in Additive Manufacturing for Copper-Based Alloys and Composites: A Comprehensive Review,” *Journal of Manufacturing and Materials Processing* **8** (2024): 54, DOI **10.3390/jmmp8020054**, identifies (a) previously deposited **CuNi2SiCr powder on cast AlBC3 NAB**, for which porosity and insufficient strengthening were flagged as repair limitations; and (b) laser-metal-deposited **Cu–9Al–5Fe–5Ni**, whose as-built martensite/Widmanstätten α/precipitates produced yield strength **593–713 MPa**, UTS **769–949 MPa** and elongation **10–12%**. The cited primary corrosion/repair article is Yao, C.-L., and Shim, D.-S., “Corrosive properties of CuNi2SiCr fabricated through directed energy deposition on a nickel-aluminum bronze substrate,” *Journal of Alloys and Compounds* **918** (2022): 165776, DOI **10.1016/j.jallcom.2022.165776**; its full corrosion methods and numerical results were **not retrievable here**. **CuNi2SiCr has about 2% Ni and contains Si**: it is **not C71500** and does not establish seawater parity for 10–30%-Ni Cu–Ni powders. **[CITE] [NUMBERS] [NAVY] [NOVELTY-RISK] [GAP]** (nemani2024advancementsinadditive pages 62-68, nemani2024advancementsinadditive pages 79-83)

8. **Distinguish elemental blends and wire from the proposed powder.** Yadav, S., Jinoop, A. N., Sinha, N., Paul, C. P., and Bindra, K. S., “Parametric investigation and characterization of laser directed energy deposited copper-nickel graded layers,” *International Journal of Advanced Manufacturing Technology* **108** (2020): 3779–3791, DOI **10.1007/s00170-020-05644-9**. **Process:** blown-powder laser DED, but **separately manufactured elemental Cu and Ni powders premixed for 18 h**, **45–105 µm**, at Cu/Ni **25/75, 50/50 or 75/25** on preheated pure Cu—not individually prealloyed powder particles, and not a seawater repair test. Graded deposits exceeded **99% relative density**; **1.2–1.8 kW**, **0.3–0.7 m/min** and **2.8 g/min** were studied. **[CITE] [NUMBERS] [NOVELTY-RISK] [GAP]** (yadav2020parametricinvestigationand pages 1-2, yadav2020parametricinvestigationand pages 2-4)

9. **Wire-arc corroboration, not powder-DED corrosion qualification.** Ding, D., Pan, Z., van Duin, S., Li, H., and Shen, C., “Fabricating Superior NiAl Bronze Components through Wire Arc Additive Manufacturing,” *Materials* **9** (2016): 652, DOI **10.3390/ma9080652**: **WAAM**, fully dense as-built NAB; **corrosion not measured** and actual experimental wt% composition not established in the available excerpt. Kim, J.-s., Kim, J., and Pyo, C., “Comparison of Mechanical Properties of Ni-Al-Bronze Alloy Fabricated through Wire Arc Additive Manufacturing with Ni-Al-Bronze Alloy Fabricated through Casting,” *Metals* **10** (2020): 1164, DOI **10.3390/met10091164**: WAAM tensile strengths **718–735 MPa**, elongation **25.1–27.7%**, hardness **196.8–218.4 HV** versus **170.8 HV cast**; **no seawater-corrosion measurement**. These results demonstrate that density, strength and hardness cannot serve as surrogates for corrosion. **[CITE] [NUMBERS] [GAP]** (ding2016fabricatingsuperiornial pages 9-12, ding2016fabricatingsuperiornial pages 1-3, kim2020comparisonofmechanical pages 12-14)

## Can short tests reproduce long-exposure rankings?

**Not demonstrated for the proposed alloy/process space.** The retrieved evidence establishes that polarization, LPR and EIS can resolve *time-dependent electrochemical behavior*, **not** that a test on a newly polished or one-day-old Cu–Ni/NAB deposit ranks candidates identically to **30-day immersion or 3–18-month natural seawater**. The 720-hour cast-NAB comparison even gives opposing numerical orderings between early electrochemical rate and gravimetric loss, albeit without a statistically significant alloy difference. In flowing natural seawater, Cu–Ni EIS resistance rose and fell substantially between days 1, 20, 30 and 180; NAB polarization shifted after 480 hours. Therefore **hours-to-days screening is particularly liable to misrank alloys throughout the first approximately 20–30 days; Cu–Ni in temperate water may need about 60–90 days to mature its film**. Neither 30 days nor 90 days guarantees mature performance under biofouling, stagnation, sulfide or different flow. **[CITE] [NUMBERS] [GAP]** (powell2004corrosionandbiofouling pages 1-4, almuhanna2010corrosionbehaviorof pages 2-4, fayanas2025nickelaluminiumbronze pages 5-7, rivero2021effectofti pages 5-6, rivero2021effectofti pages 6-8)

Use **ASTM G59** for small-overpotential polarization resistance; **ASTM G102** for converting a defensibly obtained corrosion current to a *uniform-attack-equivalent* penetration rate; **ASTM G106** for **verification of EIS equipment/algorithms, not validation of field predictivity**; and **ASTM G31** as guidance for gravimetric laboratory immersion. **ASTM D1141 substitute ocean water** is chemically more representative than plain 3.5% NaCl but still does not recreate natural biology or field flow. An evidence-generating experimental ladder would retain independent as-deposited and wrought-C71500 reference coupons at each exposure age; measure OCP/LPR/EIS nondestructively at approximately **1, 7, 20, 30, 60 and 90 days**, use polarization on *separate* coupons, and check **30-day gravimetric loss plus maximum pit/selective-phase depth**, followed by longer **natural seawater**, controlled-flow and sulfide/stagnation tests. Treat this schedule as a **proposed validation design**, not an already demonstrated predictive standard. A proposal should quantify out-of-sample *rank concordance* between inexpensive measurements and long-exposure endpoints before the function-network optimizer trusts them. **[CITE] [GAP]** (almuhanna2010corrosionbehaviorof pages 2-4, fayanas2025nickelaluminiumbronze pages 5-7, dobson2024corrosionmechanismsand pages 92-95, dobson2024corrosionmechanismsand pages 119-122, powell2004corrosionandbiofouling pages 1-4)

**Evidence limits important to state explicitly.** The retrieved papers do not establish a universal minimum protective Ni content; a validated 24-hour electrochemical predictor of 30-day immersion or multi-month natural-seawater rankings; quantitative ultrasonic-atomized-powder Hall flow/apparent-density/oxygen specifications for the proposed compositions; or a demonstrated combination of **single-stream prealloyed powder, laser DED on both cast NAB and wrought Cu–Ni, no post-build heat treatment, and C71500-or-better natural-seawater resistance**. Some directly relevant recent DED corrosion publications were identifiable by DOI but their full quantitative results could not be checked; absence of retrieved proof is **not** proof the work has never been attempted. **[GAP]** (camilleri2025coldsprayas pages 2-3, ziqiang2025lasercladdingremanufacturing pages 1-3, nemani2024advancementsinadditive pages 79-83, nemani2024advancementsinadditive pages 105-106)

## Top 5 things the PI should know

1. **Validate the long-exposure endpoint rather than assuming early-test fidelity:** film evolution changes Cu–Ni electrochemistry over approximately **2–3 months**, while one NAB comparison reverses the numerical electrochemical/immersion ordering. **[CITE] [GAP]** (powell2004corrosionandbiofouling pages 1-4, almuhanna2010corrosionbehaviorof pages 2-4, rivero2021effectofti pages 6-8)
2. **Defend novelty against existing prealloyed bronze-on-cast-bronze laser cladding** and CuNi2SiCr-on-NAB laser DED; differentiate by *measured as-deposited seawater performance, both repair substrates, and coupled composition–powder–thermal-history optimization*. **[NOVELTY-RISK]** (ziqiang2025lasercladdingremanufacturing pages 1-3, nemani2024advancementsinadditive pages 79-83)
3. **Optimize local phase chemistry and maximum penetration, not just mean j_corr, density or hardness:** welded NAB showed **1.331-mm** κIII-path penetration despite conclusions one might draw from short average-rate tests. **[CITE] [NUMBERS]** (dobson2024corrosionmechanismsand pages 143-147, fayanas2025nickelaluminiumbronze pages 5-7)
4. **Design for clean-water film formation and dirty-water challenge separately:** sulfide at **ppb** levels during commissioning, stagnation-generated SRB, biofouling and geometry-dependent shear can defeat otherwise promising clean-NaCl results. **[CITE] [NAVY]** (phull20172.18–marine pages 25-27, phull20172.18–marine pages 27-28)
5. **A lower-Ni candidate must beat C71500 under matched conditions, not by cross-paper comparison:** maintain the same surface finish, film age, natural seawater, flow and exposure time for the candidate and wrought standard; record powder chemistry/oxygen and dendrite-scale Fe/Mn/Cr segregation so that the physics-based surrogate addresses the actual deposited material. **[GAP]** (almuhanna2010corrosionbehaviorof pages 1-2, almuhanna2010corrosionbehaviorof pages 2-4, phull20172.18–marine pages 27-28, adeeko2026processingstructurepropertiesofwirearc pages 92-102)

References

1. (powell2004corrosionandbiofouling pages 1-4): C Powell. Corrosion and biofouling resistance evaluation of 90-10 copper-nickel. Unknown journal, 2004.

2. (phull20172.18–marine pages 25-27): B Phull and AA Abdullahi. 2.18 – marine corrosion. ArXiv, 2:1107-1148, Jan 2017. URL: https://doi.org/10.1016/b978-044452787-5.00046-9, doi:10.1016/b978-044452787-5.00046-9. This article has 61 citations.

3. (phull20172.18–marine pages 27-28): B Phull and AA Abdullahi. 2.18 – marine corrosion. ArXiv, 2:1107-1148, Jan 2017. URL: https://doi.org/10.1016/b978-044452787-5.00046-9, doi:10.1016/b978-044452787-5.00046-9. This article has 61 citations.

4. (fayanas2025nickelaluminiumbronze pages 1-2): Aintzane Fayanas, Angela Veiga, Alejandro Perez, Amadeu Concustell, Silvia Molas, and Nerea Ordas. Nickel aluminium bronze alloys with enhanced erosion-corrosion resistance and mechanical strength. Journal of the Japan Society of Powder and Powder Metallurgy, 72:S819-S826, Mar 2025. URL: https://doi.org/10.2497/jjspm.15f-t13-08, doi:10.2497/jjspm.15f-t13-08. This article has 1 citations.

5. (nemani2024advancementsinadditive pages 62-68): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

6. (nemani2024advancementsinadditive pages 79-83): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

7. (almuhanna2010corrosionbehaviorof pages 1-2): K. Al-Muhanna and K. Habib. Corrosion behavior of different alloys exposed to continuous flowing seawater by electrochemical impedance spectroscopy (eis). Desalination, 250:404-407, Jan 2010. URL: https://doi.org/10.1016/j.desal.2009.09.065, doi:10.1016/j.desal.2009.09.065. This article has 50 citations and is from a domain leading peer-reviewed journal.

8. (almuhanna2010corrosionbehaviorof pages 2-4): K. Al-Muhanna and K. Habib. Corrosion behavior of different alloys exposed to continuous flowing seawater by electrochemical impedance spectroscopy (eis). Desalination, 250:404-407, Jan 2010. URL: https://doi.org/10.1016/j.desal.2009.09.065, doi:10.1016/j.desal.2009.09.065. This article has 50 citations and is from a domain leading peer-reviewed journal.

9. (rivero2021effectofti pages 2-3): Pedro J. Rivero, C. Berlanga, J. F. Palacio, and M. V Biezma-Moraleda. Effect of ti on microstructure, mechanical properties and corrosion behavior of a nickel-aluminum bronze alloy. Materials Research, Jan 2021. URL: https://doi.org/10.1590/1980-5373-mr-2020-0335, doi:10.1590/1980-5373-mr-2020-0335. This article has 17 citations.

10. (rivero2021effectofti pages 5-6): Pedro J. Rivero, C. Berlanga, J. F. Palacio, and M. V Biezma-Moraleda. Effect of ti on microstructure, mechanical properties and corrosion behavior of a nickel-aluminum bronze alloy. Materials Research, Jan 2021. URL: https://doi.org/10.1590/1980-5373-mr-2020-0335, doi:10.1590/1980-5373-mr-2020-0335. This article has 17 citations.

11. (rivero2021effectofti pages 6-8): Pedro J. Rivero, C. Berlanga, J. F. Palacio, and M. V Biezma-Moraleda. Effect of ti on microstructure, mechanical properties and corrosion behavior of a nickel-aluminum bronze alloy. Materials Research, Jan 2021. URL: https://doi.org/10.1590/1980-5373-mr-2020-0335, doi:10.1590/1980-5373-mr-2020-0335. This article has 17 citations.

12. (rivero2021effectofti pages 1-2): Pedro J. Rivero, C. Berlanga, J. F. Palacio, and M. V Biezma-Moraleda. Effect of ti on microstructure, mechanical properties and corrosion behavior of a nickel-aluminum bronze alloy. Materials Research, Jan 2021. URL: https://doi.org/10.1590/1980-5373-mr-2020-0335, doi:10.1590/1980-5373-mr-2020-0335. This article has 17 citations.

13. (fayanas2025nickelaluminiumbronze pages 2-5): Aintzane Fayanas, Angela Veiga, Alejandro Perez, Amadeu Concustell, Silvia Molas, and Nerea Ordas. Nickel aluminium bronze alloys with enhanced erosion-corrosion resistance and mechanical strength. Journal of the Japan Society of Powder and Powder Metallurgy, 72:S819-S826, Mar 2025. URL: https://doi.org/10.2497/jjspm.15f-t13-08, doi:10.2497/jjspm.15f-t13-08. This article has 1 citations.

14. (fayanas2025nickelaluminiumbronze pages 5-7): Aintzane Fayanas, Angela Veiga, Alejandro Perez, Amadeu Concustell, Silvia Molas, and Nerea Ordas. Nickel aluminium bronze alloys with enhanced erosion-corrosion resistance and mechanical strength. Journal of the Japan Society of Powder and Powder Metallurgy, 72:S819-S826, Mar 2025. URL: https://doi.org/10.2497/jjspm.15f-t13-08, doi:10.2497/jjspm.15f-t13-08. This article has 1 citations.

15. (fayanas2025nickelaluminiumbronze media 84062957): Aintzane Fayanas, Angela Veiga, Alejandro Perez, Amadeu Concustell, Silvia Molas, and Nerea Ordas. Nickel aluminium bronze alloys with enhanced erosion-corrosion resistance and mechanical strength. Journal of the Japan Society of Powder and Powder Metallurgy, 72:S819-S826, Mar 2025. URL: https://doi.org/10.2497/jjspm.15f-t13-08, doi:10.2497/jjspm.15f-t13-08. This article has 1 citations.

16. (dobson2024corrosionmechanismsand pages 240-244): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

17. (dobson2024corrosionmechanismsand pages 143-147): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

18. (dobson2024corrosionmechanismsand pages 92-95): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

19. (dobson2024corrosionmechanismsand pages 151-154): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

20. (ziqiang2025lasercladdingremanufacturing pages 1-3): Pi Ziqiang, Du Kaiping, Chen Xing, Zheng Zhaoran, and Wang Chen. Laser cladding remanufacturing of propeller zcual8mn13fe3ni2 alloy. Scientific Reports, Apr 2025. URL: https://doi.org/10.1038/s41598-025-96674-4, doi:10.1038/s41598-025-96674-4. This article has 7 citations and is from a peer-reviewed journal.

21. (ziqiang2025lasercladdingremanufacturing pages 6-9): Pi Ziqiang, Du Kaiping, Chen Xing, Zheng Zhaoran, and Wang Chen. Laser cladding remanufacturing of propeller zcual8mn13fe3ni2 alloy. Scientific Reports, Apr 2025. URL: https://doi.org/10.1038/s41598-025-96674-4, doi:10.1038/s41598-025-96674-4. This article has 7 citations and is from a peer-reviewed journal.

22. (camilleri2025coldsprayas pages 12-13): Steven Camilleri, Tien Tran, Andrew Duguid, and Kannoorpatti Narayanan Krishnan. Cold spray as a powder metallurgy process for production of nickel aluminium bronze. PLOS One, 20:e0319333, Mar 2025. URL: https://doi.org/10.1371/journal.pone.0319333, doi:10.1371/journal.pone.0319333. This article has 2 citations and is from a peer-reviewed journal.

23. (nemani2024advancementsinadditive pages 71-74): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

24. (nemani2024advancementsinadditive pages 74-79): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

25. (yadav2020parametricinvestigationand pages 1-2): S. Yadav, S. Yadav, A. N. Jinoop, A. N. Jinoop, Niraj Sinha, C. Paul, C. Paul, K. Bindra, and K. Bindra. Parametric investigation and characterization of laser directed energy deposited copper-nickel graded layers. The International Journal of Advanced Manufacturing Technology, 108:3779-3791, Jun 2020. URL: https://doi.org/10.1007/s00170-020-05644-9, doi:10.1007/s00170-020-05644-9. This article has 51 citations.

26. (yadav2020parametricinvestigationand pages 2-4): S. Yadav, S. Yadav, A. N. Jinoop, A. N. Jinoop, Niraj Sinha, C. Paul, C. Paul, K. Bindra, and K. Bindra. Parametric investigation and characterization of laser directed energy deposited copper-nickel graded layers. The International Journal of Advanced Manufacturing Technology, 108:3779-3791, Jun 2020. URL: https://doi.org/10.1007/s00170-020-05644-9, doi:10.1007/s00170-020-05644-9. This article has 51 citations.

27. (ding2016fabricatingsuperiornial pages 9-12): Donghong Ding, Zengxi Pan, Stephen Van Duin, Huijun Li, and Chen Shen. Fabricating superior nial bronze components through wire arc additive manufacturing. Materials, 9:652, Aug 2016. URL: https://doi.org/10.3390/ma9080652, doi:10.3390/ma9080652. This article has 278 citations.

28. (ding2016fabricatingsuperiornial pages 1-3): Donghong Ding, Zengxi Pan, Stephen Van Duin, Huijun Li, and Chen Shen. Fabricating superior nial bronze components through wire arc additive manufacturing. Materials, 9:652, Aug 2016. URL: https://doi.org/10.3390/ma9080652, doi:10.3390/ma9080652. This article has 278 citations.

29. (kim2020comparisonofmechanical pages 12-14): Ji-sun Kim, Jaewoong Kim, and Changmin Pyo. Comparison of mechanical properties of ni-al-bronze alloy fabricated through wire arc additive manufacturing with ni-al-bronze alloy fabricated through casting. Metals, 10:1164, Aug 2020. URL: https://doi.org/10.3390/met10091164, doi:10.3390/met10091164. This article has 52 citations.

30. (dobson2024corrosionmechanismsand pages 119-122): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

31. (camilleri2025coldsprayas pages 2-3): Steven Camilleri, Tien Tran, Andrew Duguid, and Kannoorpatti Narayanan Krishnan. Cold spray as a powder metallurgy process for production of nickel aluminium bronze. PLOS One, 20:e0319333, Mar 2025. URL: https://doi.org/10.1371/journal.pone.0319333, doi:10.1371/journal.pone.0319333. This article has 2 citations and is from a peer-reviewed journal.

32. (nemani2024advancementsinadditive pages 105-106): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

33. (adeeko2026processingstructurepropertiesofwirearc pages 92-102): OO Adeeko. Processing/structure/properties of wire-arc additively manufactured 70cu-30ni alloy. Unknown journal, 2026.
