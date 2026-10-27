<!--
Edison Scientific PRECEDENT task (batch 2)
- Task ID: 96525e49-088d-443d-a4e8-6dfd0c280a00
- Submitted: 2026-10-17T05:37:06Z
- Fetched: 2026-10-17T06:09:00Z (status: success)
- Raw trajectory JSON: ../raw/b2-09-precedent-as-deposited-design.json.gz
- Synthesis: ../README.md
-->

Question:

Has anyone designed or modified the composition of nickel-aluminum bronze,
aluminum bronze, or copper-nickel so that additively manufactured material
WITHOUT post-build heat treatment matches or beats the seawater or NaCl
corrosion resistance of the heat-treated cast or wrought alloy? Has anyone
used the reheating of earlier layers during DED (intrinsic heat treatment,
interlayer temperature control) to temper NAB or remove martensite in place?
Include Jia et al., Additive Manufacturing 127 (2026) 105291 if relevant and
say what it did. Give DOIs, and state what remains undone. Exclude
publications by Sterling G. Baird.

---

Question: Has anyone designed or modified the composition of nickel-aluminum bronze,
aluminum bronze, or copper-nickel so that additively manufactured material
WITHOUT post-build heat treatment matches or beats the seawater or NaCl
corrosion resistance of the heat-treated cast or wrought alloy? Has anyone
used the reheating of earlier layers during DED (intrinsic heat treatment,
interlayer temperature control) to temper NAB or remove martensite in place?
Include Jia et al., Additive Manufacturing 127 (2026) 105291 if relevant and
say what it did. Give DOIs, and state what remains undone. Exclude
publications by Sterling G. Baird.


No. ## Assessment

**There is a qualified yes for better chloride corrosion in *as-built* material, but no verified example meeting every condition in the question.** Ti-modified wire-arc-additively-manufactured (WAAM) nickel–aluminum bronze (NAB) outperformed an *unmodified as-deposited* NAB control, not a heat-treated cast or wrought control. Separately, as-built WAAM 70/30 copper–nickel outperformed a **wrought** plate in 3.5 wt.% NaCl, but the plate’s heat-treatment state was not documented and the experiment was not a controlled composition-design study. I found no verified aluminum-bronze-only example satisfying the full comparison. These distinctions matter because better corrosion than *as-cast* or untreated AM material does not establish parity with **heat-treated** conventional material. (zhang2026effectoflowlevel pages 13-16, song2024microstructuresandcorrosion pages 1-2, song2024microstructuresandcorrosion pages 10-13, jafari2021effectoffluid pages 2-4)

The following evidence matrix separates those partial successes from the requested benchmark. Zhang et al.’s electrochemical results were also checked against the cropped original Table 4. (zhang2026effectoflowlevel pages 13-16, zhang2026effectoflowlevel media 2d5f87b2)

| Study and DOI | Exact intervention | As-built corrosion observation | Comparator | Passes strict benchmark?* |
|---|---|---|---|---|
| Jia et al., *Additive Manufacturing* 127 (2026) 105291. DOI: [10.1016/j.addma.2026.105291](https://doi.org/10.1016/j.addma.2026.105291) | “Subtractive composition design” of laser-additively-manufactured NAB; the inaccessible primary text prevents verification of the alloy recipe. | Title/metadata claim superior as-deposited mechanical and corrosion performance, but the numerical corrosion results and test conditions could not be verified. | Comparator identity and condition are unverified. Because the paper was inaccessible, success cannot be excluded, but neither can a heat-treated cast/wrought, same-electrolyte comparison be confirmed. (zhang2026effectoflowlevel pages 20-20, huo2025modulatingheatinput pages 1-2) | **Unverified—not countable as a demonstrated pass from accessible evidence.** |
| Zhang et al. (2026). DOI: [10.1007/s44500-026-00016-x](https://doi.org/10.1007/s44500-026-00016-x) | Added 0.03, 0.05, or 0.1 wt.% Ti nanoparticles between WAAM-NAB layers; no post-build heat treatment. | In 3.5 wt.% NaCl, 0.1 wt.% Ti reduced \(i_{corr}\) from 10.06 to 8.49 µA/cm² (15.6%) and shifted \(E_{corr}\) from −192.91 to −188.57 mV versus SCE. (zhang2026effectoflowlevel pages 13-16, zhang2026effectoflowlevel media 2d5f87b2) | Unmodified as-deposited WAAM-NAB only; no heat-treated cast or wrought control. | **No:** composition modification succeeded relative to the AM control, but the required conventional heat-treated benchmark was absent. |
| Song et al. (2024). DOI: [10.3390/ma17040876](https://doi.org/10.3390/ma17040876) | Process-parameter optimization of as-built WAAM 70/30 Cu–Ni; sample 6 used 8 m/min wire feed, 1000 mm/min travel, 3.85 mm track spacing, and 150–200 °C interpass temperature. Wire also contained 0.25 wt.% Ti and 0.1 wt.% Si absent from the plate, but this was not presented as deliberate composition design. (song2024microstructuresandcorrosion pages 1-2, song2024microstructuresandcorrosion pages 2-5) | In 3.5 wt.% NaCl, sample 6 exceeded wrought-film resistance: XY \(R_f\) 1.40 versus 1.08 × 10⁵ Ω and YZ 1.66 versus 1.18 × 10⁵ Ω; it also had higher breakdown potential and lower passive-current density. (song2024microstructuresandcorrosion pages 10-13) | Wrought C71500 plate; no heat treatment of that plate was documented, and feed wire/plate minor-element chemistries differed. | **Near miss, not strict pass:** as-built AM beat wrought material in the same electrolyte, but the wrought comparator was not documented as heat-treated and the work was not a controlled composition-redesign study. |
| Huo et al. (2025). DOI: [10.3390/ma18102205](https://doi.org/10.3390/ma18102205) | Varied CMT-AM NAB heat input from 243.8 to 644.7 J/mm while holding interlayer temperature below 50 °C; no alloy-composition redesign. | In 3.5 wt.% NaCl, increasing heat input worsened \(i_{corr}\) from 2.56 ± 0.04 to 7.52 ± 0.07 µA/cm². The deposits were reported to contain no residual β or martensitic β′. (huo2025modulatingheatinput pages 10-13, huo2025modulatingheatinput pages 5-7, huo2025modulatingheatinput pages 2-4) | Internal comparison among as-CMTAM heat-input conditions; no cast, wrought, or heat-treated conventional control. | **No:** useful process/thermal-control evidence, but neither composition modification nor the required conventional benchmark was tested. |
| Ding et al. (2016). DOI: [10.3390/ma9080652](https://doi.org/10.3390/ma9080652) | WAAM NAB exhibited intrinsic reheated layer bands, but martensite removal/refinement was achieved by post-build annealing at 675 °C for 6 h followed by air cooling. (ding2016fabricatingsuperiornial pages 3-6, ding2016fabricatingsuperiornial pages 6-9) | No corrosion test was performed; corrosion evaluation was explicitly left for future work. (ding2016fabricatingsuperiornial pages 9-12) | Mechanical comparison with as-cast base metal; no chloride-corrosion comparator. | **No:** it neither remained without post-build heat treatment nor demonstrated corrosion parity. |
| **Strict benchmark applied** | **Deliberately modified NAB, aluminum-bronze, or Cu–Ni composition; tested in the as-built state without post-build heat treatment.** | **Corrosion must match or beat the reference in seawater or NaCl.** | **Reference must be explicitly heat-treated cast or wrought material tested under the same electrolyte/protocol.** | **None of the accessible non-Baird studies unambiguously passes all requirements; Jia et al. remains unresolved because its primary text was inaccessible.** |


*Table: Non-Baird studies are screened against the full requirement: deliberate composition modification, no post-build heat treatment, and a same-electrolyte comparison with explicitly heat-treated cast or wrought material. Accessible evidence shows promising partial results, but no unambiguous strict pass; Jia et al. remains unverifiable.*

**Jia et al. is particularly relevant, but cannot be scored as a verified pass.** The bibliographic record identifies Zhiyuan Jia and colleagues, “*Subtractive composition design of nickel-aluminum bronze for laser additive manufacturing: achieving superior as-deposited mechanical and corrosion performance*,” *Additive Manufacturing* **127** (2026), 105291, DOI **10.1016/j.addma.2026.105291**. Its title establishes that the authors pursued *subtractive composition design* and claimed superior *as-deposited* properties. The paper itself was not retrievable for this assessment: its elemental changes, corrosion medium and measurements, and—decisively—whether its comparator was **heat-treated cast or wrought NAB tested under the same conditions** remain unverified. Thus Jia must not be overlooked, but its title alone cannot resolve the user’s strict question. (zhang2026effectoflowlevel pages 20-20)

For the strongest accessible **composition** result, Zhang et al. added **0.03, 0.05, or 0.1 wt.% Ti** to WAAM NAB. In 3.5 wt.% NaCl, **0.1 wt.% Ti** lowered corrosion-current density from **10.06 to 8.49 µA cm⁻²**, a **15.6%** reduction, relative to Ti-free as-deposited WAAM NAB; the 0.03 wt.% addition instead raised it to **10.88 µA cm⁻²**. There was **no heat-treated cast/wrought test specimen**. DOI **10.1007/s44500-026-00016-x**. (zhang2026effectoflowlevel pages 13-16, zhang2026effectoflowlevel media 2d5f87b2)

For the closest accessible **conventional-material corrosion comparison**, Song et al. used as-built WAAM **70/30 Cu–Ni** and a **wrought C71500 plate** in 3.5 wt.% NaCl. Their best WAAM condition had fitted corrosion-film resistances of **1.40 versus 1.08 × 10⁵ Ω** on the XY plane and **1.66 versus 1.18 × 10⁵ Ω** on the YZ plane, and also showed favorable breakdown potential and passive current density. The wire contained **0.25 wt.% Ti and 0.1 wt.% Si**, absent from the plate, so composition was not identical; however, the authors varied *deposition parameters*, not Ti/Si content as a designed alloy experiment. They describe the plate as wrought, **not explicitly heat-treated**. DOI **10.3390/ma17040876**. (song2024microstructuresandcorrosion pages 1-2, song2024microstructuresandcorrosion pages 10-13, song2024microstructuresandcorrosion pages 2-5)

## Has layer reheating replaced NAB heat treatment?

**Not as a demonstrated, controlled in-place tempering process with the requested corrosion validation.** Ding et al. observed ∼**200-µm reheated bands** in WAAM NAB, yet as-deposited metal still contained fine martensite and reheating near the fusion line could *create* martensite. Their α-plus-κ refinement and martensite replacement followed a **separate 675 °C, six-hour post-build treatment**; they performed no corrosion experiment. DOI **10.3390/ma9080652**. (ding2016fabricatingsuperiornial pages 3-6, ding2016fabricatingsuperiornial pages 6-9, ding2016fabricatingsuperiornial pages 9-12)

Huo et al. controlled interlayer temperature to **≤50 °C** while varying CMT-AM NAB heat input. They reported **no residual β or β′ martensite** in the examined deposits, and lower heat input improved corrosion current density in 3.5 wt.% NaCl (**2.56 ± 0.04 versus 7.52 ± 0.07 µA cm⁻²** at **243.8 versus 644.7 J mm⁻¹**). This demonstrates an *as-deposited, reportedly martensite-free microstructure*, **not** that measured reheating of an earlier, demonstrably martensitic layer tempered that martensite in place; it also lacks a heat-treated conventional corrosion control. DOI **10.3390/ma18102205**. (huo2025modulatingheatinput pages 10-13, huo2025modulatingheatinput pages 2-4, huo2025modulatingheatinput pages 5-7)

**What remains undone:** Verify Jia et al.’s full methods and comparator before claiming a definitive literature-wide negative or positive answer. Then test an intentionally composition-designed, **un-heat-treated** AM NAB, aluminum bronze, or Cu–Ni against explicitly **heat-treated cast or wrought** specimens in the **same** NaCl or seawater exposure, including immersion and localized-corrosion endpoints rather than relying only on short electrochemical tests. To establish intrinsic DED tempering specifically, measure earlier layers’ thermal histories and β′ fractions **before and after subsequent passes**, deliberately vary interpass temperature/reheating, assess the last layer that receives no further pass, and pair the resulting phase maps with matched corrosion testing. Conventional C95800 provides a meaningful reason to set a demanding control: a separate study found that **675 °C for six hours** reduced its corrosion-sensitive β fraction and improved resistance in 3.5 wt.% NaCl, including under flow; that study did **not** compare AM material. DOI **10.3390/cmd2010004**. (ding2016fabricatingsuperiornial pages 3-6, huo2025modulatingheatinput pages 10-13, zhang2026effectoflowlevel media 2d5f87b2, jafari2021effectoffluid pages 2-4, jafari2021effectoffluid pages 4-7)

References

1. (zhang2026effectoflowlevel pages 13-16): La-Mei Zhang, Xiao-Yu Cai, Bai-Long Song, Bo-Lun Dong, San-Wai Lin, and Fuad Khoshnaw. Effect of low-level ti microalloying on the microstructure, mechanical properties, and corrosion behaviour of waam-processed nickel-aluminium bronze. Advanced Materials Joining, Oct 2026. URL: https://doi.org/10.1007/s44500-026-00016-x, doi:10.1007/s44500-026-00016-x. This article has 0 citations.

2. (song2024microstructuresandcorrosion pages 1-2): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

3. (song2024microstructuresandcorrosion pages 10-13): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

4. (jafari2021effectoffluid pages 2-4): Hamid Reza Jafari, Ali Davoodi, and Saman Hosseinpour. Effect of fluid flow on the corrosion performance of as-cast and heat-treated nickel aluminum bronze alloy (uns c95800) in saline solution. Corrosion and Materials Degradation, 2:61-77, Feb 2021. URL: https://doi.org/10.3390/cmd2010004, doi:10.3390/cmd2010004. This article has 12 citations.

5. (zhang2026effectoflowlevel media 2d5f87b2): La-Mei Zhang, Xiao-Yu Cai, Bai-Long Song, Bo-Lun Dong, San-Wai Lin, and Fuad Khoshnaw. Effect of low-level ti microalloying on the microstructure, mechanical properties, and corrosion behaviour of waam-processed nickel-aluminium bronze. Advanced Materials Joining, Oct 2026. URL: https://doi.org/10.1007/s44500-026-00016-x, doi:10.1007/s44500-026-00016-x. This article has 0 citations.

6. (zhang2026effectoflowlevel pages 20-20): La-Mei Zhang, Xiao-Yu Cai, Bai-Long Song, Bo-Lun Dong, San-Wai Lin, and Fuad Khoshnaw. Effect of low-level ti microalloying on the microstructure, mechanical properties, and corrosion behaviour of waam-processed nickel-aluminium bronze. Advanced Materials Joining, Oct 2026. URL: https://doi.org/10.1007/s44500-026-00016-x, doi:10.1007/s44500-026-00016-x. This article has 0 citations.

7. (huo2025modulatingheatinput pages 1-2): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

8. (song2024microstructuresandcorrosion pages 2-5): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

9. (huo2025modulatingheatinput pages 10-13): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

10. (huo2025modulatingheatinput pages 5-7): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

11. (huo2025modulatingheatinput pages 2-4): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

12. (ding2016fabricatingsuperiornial pages 3-6): Donghong Ding, Zengxi Pan, Stephen Van Duin, Huijun Li, and Chen Shen. Fabricating superior nial bronze components through wire arc additive manufacturing. Materials, 9:652, Aug 2016. URL: https://doi.org/10.3390/ma9080652, doi:10.3390/ma9080652. This article has 278 citations.

13. (ding2016fabricatingsuperiornial pages 6-9): Donghong Ding, Zengxi Pan, Stephen Van Duin, Huijun Li, and Chen Shen. Fabricating superior nial bronze components through wire arc additive manufacturing. Materials, 9:652, Aug 2016. URL: https://doi.org/10.3390/ma9080652, doi:10.3390/ma9080652. This article has 278 citations.

14. (ding2016fabricatingsuperiornial pages 9-12): Donghong Ding, Zengxi Pan, Stephen Van Duin, Huijun Li, and Chen Shen. Fabricating superior nial bronze components through wire arc additive manufacturing. Materials, 9:652, Aug 2016. URL: https://doi.org/10.3390/ma9080652, doi:10.3390/ma9080652. This article has 278 citations.

15. (jafari2021effectoffluid pages 4-7): Hamid Reza Jafari, Ali Davoodi, and Saman Hosseinpour. Effect of fluid flow on the corrosion performance of as-cast and heat-treated nickel aluminum bronze alloy (uns c95800) in saline solution. Corrosion and Materials Degradation, 2:61-77, Feb 2021. URL: https://doi.org/10.3390/cmd2010004, doi:10.3390/cmd2010004. This article has 12 citations.
