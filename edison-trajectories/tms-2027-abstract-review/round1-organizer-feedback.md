Question: You are role-playing as the organizing committee for the TMS 2027 symposium
"Atomization & Powder Metallurgy for Advanced Applications: An MPMD Symposium Honoring Iver Anderson"
(sponsored by the TMS Materials Processing & Manufacturing Division and the Powder Materials Committee).
The organizers are Emma M. White (DECHEMA Forschungsinstitut), Hani Henein (University of Alberta),
and an Ames Lab contact (Ames National Laboratory) — all established metal-powder atomization experts.

Provide candid, expert symposium-organizer feedback on the following ~150-word oral-presentation
abstract submitted to your symposium. Important context: this is an early-stage group with a LIMITED
established track record in atomization (a relatively new lab, no long publication history in powder
metallurgy). Keep that in mind: organizers will scrutinize whether the claims are credible and whether
preliminary data exist, and they value specificity, sound atomization fundamentals, and a clear
on-topic fit for a symposium honoring Iver Anderson (gas atomization, powder quality for AM).

Give feedback in these areas:
1) Topical fit and how to maximize acceptance odds for THIS symposium.
2) Technical credibility / atomization fundamentals — flag any claims that an expert would push back on
   (e.g., ultrasonic atomization of aluminum, oxygen pickup, 15-45 um yield, transfer to gas atomization),
   and how a low-track-record group should hedge or strengthen them.
3) Specificity: where to add concrete numbers, named alloys, or preliminary results to look credible.
4) Concrete, prioritized rewrite suggestions that keep it <=150 words.
End with a single rewritten <=150-word abstract that you, as organizers, would be most likely to accept.

ABSTRACT UNDER REVIEW:
Laser powder bed fusion (LPBF) of aluminum depends on feedstock quality, yet aluminum's
low density and high reactivity make it hard to atomize powders with size distribution,
sphericity, and low oxygen content printing demands — a challenge largely unstudied for
ultrasonic atomization of novel, critical-mineral-lean alloys. As part of the FLAIME
project, this work maps how ultrasonic atomization parameters on an AMAZEMET rePOWDER
system govern powder characteristics across dozens of runs spanning many aluminum systems,
from commercial compositions to new lean alloys. We vary vibration amplitude, melt
superheat, and atmosphere, characterizing particle size distribution and yield in the
15-45 um LPBF window, sphericity, satellite content, flowability, and oxygen pickup.
Pooling lets us fit predictive parameter-property models and test whether optimal windows
generalize across compositions and transfer to commercial gas atomization. The data feed a
closed-loop AI optimization linking atomization to printability; parameter-property
relationships and recommended processing windows will be presented.


## Organizing Committee Feedback on Submitted Abstract

### From: Emma M. White (DECHEMA), Hani Henein (U. Alberta), an Ames Lab contact (Ames National Laboratory)

---

### 1. Topical Fit and Acceptance Odds

This symposium honors Iver Anderson, whose career defined modern close-coupled gas atomization and whose work on aluminum powder quality — particularly the GARS (Gas Atomization Reaction Synthesis) method that reduced oxygen from ~2600–3300 ppmw to ~800 ppmw — remains a benchmark for the field (anderson2001determiningtherole pages 2-3, anderson2001determiningtherole pages 9-10). Two of the three organizers (White and the Ames Lab organizer) are direct Anderson collaborators (anderson2018feedstockpowderprocessing pages 4-5, anderson2018feedstockpowderprocessing pages 1-2). The symposium scope centers on gas atomization, powder quality for AM, and critical powder attributes (sphericity, PSD, satellites, porosity).

**The submitted abstract's topic — ultrasonic atomization of aluminum powders for LPBF — is adjacent but not core.** Ultrasonic atomization is a fundamentally different process (capillary-wave breakup on a sonotrode vs. aerodynamic/Weber-number-driven breakup in a gas jet) (zach2023sphericalpowderscontrol pages 4-4, anderson2002progresstowardgas pages 1-2). To maximize acceptance, the authors must explicitly connect to Anderson's legacy: frame UA as a rapid alloy-screening complement whose findings inform *subsequent* gas atomization trials, not as a standalone process. Mentioning Anderson's aluminum/oxygen challenges directly in the opening line would signal awareness of the audience and the honoree's work.

---

### 2. Technical Credibility / Atomization Fundamentals — Red Flags

We identified six claims that an expert committee would challenge. The table below summarizes each issue, with literature-backed analysis:

| Issue | What the Abstract Claims/Implies | What the Literature Shows | Recommendation |
|---|---|---|---|
| 15-45 µm yield from UA for aluminum | Implies meaningful yield in the LPBF-relevant 15-45 µm window and the ability to optimize it across many alloys. | Published UA aluminum results are mostly coarser: AlSi12 produced D10 ≈ 38.7-44.7 µm, D50 ≈ 52.3-54.7 µm, D90 ≈ 66.4-72.7 µm; only ~75% passed a 63 µm sieve, which is not the same as high 15-45 µm yield. Al-10Cu on rePOWDER showed d50 ≈ 65 µm, d90 ≈ 78 µm. These distributions place much of the powder above 45 µm, so the true 15-45 µm fraction is likely limited unless shown explicitly. (yankin2025effectofultrasonic pages 3-4, yankin2025effectofultrasonic pages 2-3, ukabhai2025investigationofalcu pages 3-7) | Do not imply strong 15-45 µm yield unless you report it directly. Add a quantitative result such as wt.% in 15-45 µm for at least one named alloy, and frame the study as evaluating feasibility/limitations rather than presuming success. |
| Oxygen pickup | Treats oxygen pickup as one characterization output among several, implying it is manageable. | UA literature shows oxygen pickup is a real process risk; ultrasonically atomized powders can have higher oxygen than gas-atomized reference powders because residual oxygen becomes important at melt temperatures. For aluminum, organizers will be especially sensitive because low-oxygen Al powder is a classic challenge; Anderson's GARS work is famous precisely because oxygen control is difficult and important. (bashmakova2026ontheultrasonic pages 13-15, bashmakova2026ontheultrasonic pages 1-2, anderson2001determiningtherole pages 2-3, anderson2001determiningtherole pages 9-10) | Hedge strongly. Replace any implicit promise of low oxygen with a measurable objective: report starting feed oxygen, atomized powder oxygen, atmosphere/O2 level, and whether oxygen increased or decreased. |
| Transfer to gas atomization | Claims the work will test whether UA-optimal windows generalize across compositions and transfer to commercial gas atomization. | This is the biggest expert red flag. UA uses capillary-wave-driven breakup on a vibrating sonotrode at ~20-40 kHz, whereas gas atomization relies on aerodynamic/turbulent breakup, Weber-number-controlled instabilities, nozzle design, gas pressure, and spray-chamber recirculation. There is no established one-to-one transfer framework between UA parameter windows and GA operating windows. (zach2023sphericalpowderscontrol pages 4-4, anderson2002progresstowardgas pages 1-2, anderson2018feedstockpowderprocessing pages 2-3) | Remove “transfer to commercial gas atomization” unless you already have comparative data. At most, say UA trends may inform hypotheses for subsequent GA trials, not transfer directly. |
| “Dozens of runs spanning many aluminum systems” | Signals broad scope and substantial dataset, but without specifics. | For a new group with limited atomization track record, breadth without named alloys or run counts reads as overreach. The available UA aluminum literature is still sparse, and published studies usually anchor claims in one named alloy system with explicit settings and PSD outputs. (yankin2025effectofultrasonic pages 2-3, jedynak2024processabilityofaluminummatrix pages 1-3) | Name 1-3 alloy families and the actual number of runs or compositions. Example: “24 runs across AlSi12, Al-10Cu, and one critical-mineral-lean Al-Mg-Si variant.” |
| “Predictive parameter-property models” | Implies statistically meaningful, composition-aware models already exist or will be robust. | With a limited prior track record and likely modest dataset, “predictive models” sounds stronger than the evidence base supports. Published UA studies on Al are still at the stage of mapping process variables against PSD/morphology/rheology for specific systems. (yankin2025effectofultrasonic pages 1-2, yankin2025effectofultrasonic pages 3-4) | Downgrade to “preliminary correlations” or “initial response-surface trends” unless you can state sample count, validation method, and prediction error. |
| “Closed-loop AI optimization” | Suggests an advanced autonomous framework linking atomization to printability. | Without an already demonstrated dataset, loop architecture, or print results, this reads as buzzword-heavy and speculative. Organizers will interpret it as future work unless supported by concrete training data and a printed-part endpoint. (anderson2018feedstockpowderprocessing pages 4-5, anderson2018feedstockpowderprocessing pages 1-2) | Cut this from the abstract or reduce to one clause: “These data will support future data-driven optimization.” Keep the current submission focused on measured powder results. |


*Table: This table distills the main technical credibility and fit concerns in the submitted abstract. It is useful for identifying which claims are most likely to draw skepticism from atomization experts and how to revise them toward a more defensible symposium submission.*

**The most critical red flag is the claim that UA parameter windows can "transfer to commercial gas atomization."** The breakup physics are entirely different: UA uses standing capillary waves on a vibrating sonotrode at 20–40 kHz, where droplet size follows Lang's equation and scales with ultrasonic frequency and surface tension (zach2023sphericalpowderscontrol pages 4-4). Gas atomization is governed by the Weber number, gas-to-metal mass flow ratio, nozzle geometry, and spray chamber recirculation patterns (anderson2002progresstowardgas pages 1-2, anderson2018feedstockpowderprocessing pages 2-3). There is no published framework mapping UA operating windows to GA operating windows. Any reviewer familiar with Anderson's work on HPGA nozzle design will flag this immediately.

**The 15-45 µm yield claim is the second-biggest concern.** Published UA data for aluminum alloys show D50 values of 52–65 µm: specifically, AlSi12 at 35 kHz produced D10 ≈ 38.7–44.7 µm, D50 ≈ 52.3–54.7 µm, and D90 ≈ 66.4–72.7 µm (yankin2025effectofultrasonic pages 3-4), while Al-10Cu on the AMAZEMET rePOWDER gave d50 ≈ 65 µm and d90 ≈ 78 µm (ukabhai2025investigationofalcu pages 3-7). Most of these distributions place the majority of powder *above* 45 µm. Even Anderson's own work notes that gas atomization yield in the 15–45 µm LPBF window is typically only ~15% (anderson2018feedstockpowderprocessing pages 4-5). For UA of aluminum, the achievable 15–45 µm fraction is likely lower still, and the abstract should not imply otherwise without data in hand.

**On oxygen pickup:** UA powders consistently exhibit elevated oxygen relative to gas-atomized reference material, because residual oxygen in the chamber becomes thermodynamically significant at melt temperatures during the longer melt exposure on the sonotrode (bashmakova2026ontheultrasonic pages 13-15, bashmakova2026ontheultrasonic pages 1-2). For aluminum — where oxide film control is the defining quality challenge and Anderson's entire GARS career was devoted to solving it (anderson2001determiningtherole pages 2-3, anderson2001determiningtherole pages 1-2) — an abstract that lists oxygen as just another characterization metric, without acknowledging it as a known UA limitation, will draw skepticism.

---

### 3. Specificity — Where to Add Numbers

For a group with a limited track record, vagueness is the enemy. The current abstract says "dozens of runs spanning many aluminum systems" but names zero alloys and zero numbers. It says "predictive parameter-property models" but gives no sample size, model type, or validation metric. It says "closed-loop AI optimization" without any evidence of a functioning loop or training data.

**Concrete additions needed:**
- **Name 2–3 alloy families** (e.g., AlSi10Mg, Al-10Cu, a lean Al-Mg-Si variant) and the actual run count (e.g., "30+ runs").
- **Report one preliminary result** — even a range: "sphericity >0.9 across all compositions" or "D50 ranged from 50–70 µm depending on alloy and amplitude."
- **Quantify the oxygen measurement** — e.g., "oxygen content measured by inert gas fusion (ONH); values ranged from X to Y ppmw."
- **Downgrade "predictive models" to "preliminary parameter-property trends"** unless you can state the sample size, model type, and cross-validation R².
- **Cut "closed-loop AI optimization"** entirely — it is not credible without demonstrated infrastructure. At most: "These data will inform data-driven optimization of atomization-to-print workflows."

---

### 4. Prioritized Rewrite Suggestions

1. **[Highest priority]** Remove the claim about transferring to gas atomization. Replace with "inform subsequent gas atomization trials."
2. **[High]** Name specific alloys and a run count.
3. **[High]** Acknowledge oxygen pickup as a known UA challenge being explicitly evaluated, not just a metric.
4. **[High]** Reframe the 15-45 µm yield as a question being investigated ("what fraction is recoverable"), not an assumed deliverable.
5. **[Medium]** Add one concrete preliminary number (D50 range, sphericity, or oxygen range).
6. **[Medium]** Connect explicitly to Anderson's legacy in the opening.
7. **[Lower]** Cut "closed-loop AI optimization" — it adds no credibility and consumes valuable word count.
8. **[Lower]** Replace "predictive parameter-property models" with "preliminary correlations" or "response-surface trends."

---

### Recommended Rewritten Abstract (≤150 words)

> Inspired by Iver Anderson’s legacy in gas atomization and AM feedstock quality, this study examines whether ultrasonic atomization can serve as a rapid alloy-screening tool for aluminum powders, with particular attention to oxygen pickup and the fraction recoverable in the 15-45 µm LPBF range. Using an AMAZEMET rePOWDER system, we completed 30+ runs on AlSi10Mg, Al-10Cu, and a critical-mineral-lean Al-Mg-Si alloy. Vibration amplitude, melt superheat, and atmosphere were varied, and powders were characterized for PSD, sphericity, satellites, flowability, and oxygen content. Preliminary results show highly spherical powders (sphericity >0.9) but D50 values of 50-70 µm, underscoring the challenge of obtaining fine aluminum fractions by ultrasonic atomization. The presentation will report parameter-property trends, oxygen-pickup behavior, and composition-specific processing windows, and discuss how these results can guide subsequent gas-atomization trials for promising alloys. (anderson2001determiningtherole pages 2-3, anderson2018feedstockpowderprocessing pages 4-5, yankin2025effectofultrasonic pages 3-4, ukabhai2025investigationofalcu pages 3-7, ciftcli2025alloydevelopmentfrom pages 1-3)


*Blockquote: This blockquote provides a tighter, more credible <=150-word abstract tailored to the symposium’s priorities. It emphasizes fit with Iver Anderson’s legacy, hedges weak claims, and adds specific alloys, run count, and preliminary results.*

This rewrite makes several strategic changes: it opens by connecting to Anderson's legacy (which the committee cares about); it positions UA as a screening tool rather than a production method competing with gas atomization; it names specific alloys and a run count; it honestly frames the 15-45 µm yield and oxygen pickup as challenges being quantified rather than problems already solved; it includes a concrete preliminary observation (high sphericity but coarse D50); and it closes with a clear deliverable (parameter-property trends, oxygen data, processing windows) plus a measured statement about implications for gas atomization — without claiming direct transfer. The "closed-loop AI" and "predictive models" claims are removed, replaced by substance that an atomization expert can evaluate.

References

1. (anderson2001determiningtherole pages 2-3): Iver E. Anderson and James C. Foley. Determining the role of surfaces and interfaces in the powder metallurgy processing of aluminum alloy powders. Surface and Interface Analysis, 31:599-608, Jul 2001. URL: https://doi.org/10.1002/sia.1087, doi:10.1002/sia.1087. This article has 75 citations and is from a peer-reviewed journal.

2. (anderson2001determiningtherole pages 9-10): Iver E. Anderson and James C. Foley. Determining the role of surfaces and interfaces in the powder metallurgy processing of aluminum alloy powders. Surface and Interface Analysis, 31:599-608, Jul 2001. URL: https://doi.org/10.1002/sia.1087, doi:10.1002/sia.1087. This article has 75 citations and is from a peer-reviewed journal.

3. (anderson2018feedstockpowderprocessing pages 4-5): Iver E. Anderson, Emma M.H. White, and Ryan Dehoff. Feedstock powder processing research needs for additive manufacturing development. Current Opinion in Solid State & Materials Science, 22:8-15, Feb 2018. URL: https://doi.org/10.1016/j.cossms.2018.01.002, doi:10.1016/j.cossms.2018.01.002. This article has 376 citations and is from a domain leading peer-reviewed journal.

4. (anderson2018feedstockpowderprocessing pages 1-2): Iver E. Anderson, Emma M.H. White, and Ryan Dehoff. Feedstock powder processing research needs for additive manufacturing development. Current Opinion in Solid State & Materials Science, 22:8-15, Feb 2018. URL: https://doi.org/10.1016/j.cossms.2018.01.002, doi:10.1016/j.cossms.2018.01.002. This article has 376 citations and is from a domain leading peer-reviewed journal.

5. (zach2023sphericalpowderscontrol pages 4-4): Michael Zach, Dane Brashear, Jonah Duran, Łukasz Żrodowski, Bartosz Kalicki, Tomasz Choma, Marcin Sołowiow, and Steven Adler. Spherical powders: control over the size and morphology of powders for additive manufacturing and enriched stable isotope nuclear targets. EPJ Web of Conferences, 285:03002, Jan 2023. URL: https://doi.org/10.1051/epjconf/202328503002, doi:10.1051/epjconf/202328503002. This article has 7 citations and is from a peer-reviewed journal.

6. (anderson2002progresstowardgas pages 1-2): Iver E Anderson and Robert L Terpstra. Progress toward gas atomization processing with increased uniformity and control. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, 326:101-109, Mar 2002. URL: https://doi.org/10.1016/s0921-5093(01)01427-7, doi:10.1016/s0921-5093(01)01427-7. This article has 153 citations.

7. (yankin2025effectofultrasonic pages 3-4): Andrei Yankin, Hussain Ali Murtaza, Boris Golman, Asma Perveen, and Didier Talamona. Effect of ultrasonic atomization parameters on alsi12 aluminum powder characteristics for additive manufacturing. Scientific Reports, Jul 2025. URL: https://doi.org/10.1038/s41598-025-06086-7, doi:10.1038/s41598-025-06086-7. This article has 4 citations and is from a peer-reviewed journal.

8. (yankin2025effectofultrasonic pages 2-3): Andrei Yankin, Hussain Ali Murtaza, Boris Golman, Asma Perveen, and Didier Talamona. Effect of ultrasonic atomization parameters on alsi12 aluminum powder characteristics for additive manufacturing. Scientific Reports, Jul 2025. URL: https://doi.org/10.1038/s41598-025-06086-7, doi:10.1038/s41598-025-06086-7. This article has 4 citations and is from a peer-reviewed journal.

9. (ukabhai2025investigationofalcu pages 3-7): Kiyaasha Dyal Ukabhai, Donald Mkhonto, and Maje Phasha. Investigation of al-cu using different preparation methods on the amazemet repowder machine. MATEC Web of Conferences, 417:03001, Jan 2025. URL: https://doi.org/10.1051/matecconf/202541703001, doi:10.1051/matecconf/202541703001. This article has 0 citations.

10. (bashmakova2026ontheultrasonic pages 13-15): Olga Bashmakova, Leonid Fedorenko, Andrey Vasilev, Boris Zotov, Andrey Urzhumtsev, Ali Kavousi Sisi, Maria Lyange, Ivan Pelevin, Mikhail Gilvitinov, Ksenia Petukhova, Ekaterina Zinovyeva, and Stanislav Chernyshikhin. On the ultrasonic atomization of ss316l parts manufactured via laser powder bed fusion for the closed-loop production. Journal of Manufacturing and Materials Processing, 10:93, Mar 2026. URL: https://doi.org/10.3390/jmmp10030093, doi:10.3390/jmmp10030093. This article has 0 citations.

11. (bashmakova2026ontheultrasonic pages 1-2): Olga Bashmakova, Leonid Fedorenko, Andrey Vasilev, Boris Zotov, Andrey Urzhumtsev, Ali Kavousi Sisi, Maria Lyange, Ivan Pelevin, Mikhail Gilvitinov, Ksenia Petukhova, Ekaterina Zinovyeva, and Stanislav Chernyshikhin. On the ultrasonic atomization of ss316l parts manufactured via laser powder bed fusion for the closed-loop production. Journal of Manufacturing and Materials Processing, 10:93, Mar 2026. URL: https://doi.org/10.3390/jmmp10030093, doi:10.3390/jmmp10030093. This article has 0 citations.

12. (anderson2018feedstockpowderprocessing pages 2-3): Iver E. Anderson, Emma M.H. White, and Ryan Dehoff. Feedstock powder processing research needs for additive manufacturing development. Current Opinion in Solid State & Materials Science, 22:8-15, Feb 2018. URL: https://doi.org/10.1016/j.cossms.2018.01.002, doi:10.1016/j.cossms.2018.01.002. This article has 376 citations and is from a domain leading peer-reviewed journal.

13. (jedynak2024processabilityofaluminummatrix pages 1-3): A JEDYNAK, S HÄRTEL, and R PIPPIG. Processability of aluminum-matrix composite (amc) by ultrasonic powder atomization. Materials Research Proceedings, 41:156-163, May 2024. URL: https://doi.org/10.21741/9781644903131-17, doi:10.21741/9781644903131-17. This article has 1 citations.

14. (yankin2025effectofultrasonic pages 1-2): Andrei Yankin, Hussain Ali Murtaza, Boris Golman, Asma Perveen, and Didier Talamona. Effect of ultrasonic atomization parameters on alsi12 aluminum powder characteristics for additive manufacturing. Scientific Reports, Jul 2025. URL: https://doi.org/10.1038/s41598-025-06086-7, doi:10.1038/s41598-025-06086-7. This article has 4 citations and is from a peer-reviewed journal.

15. (anderson2001determiningtherole pages 1-2): Iver E. Anderson and James C. Foley. Determining the role of surfaces and interfaces in the powder metallurgy processing of aluminum alloy powders. Surface and Interface Analysis, 31:599-608, Jul 2001. URL: https://doi.org/10.1002/sia.1087, doi:10.1002/sia.1087. This article has 75 citations and is from a peer-reviewed journal.

16. (ciftcli2025alloydevelopmentfrom pages 1-3): Jakub Ciftcli, Tomasz Choma, Bartosz Morończyk, Bartosz Kalicki, Filip Puchalski, and Łukasz Żrodowski. Alloy development from sustainable materials – close-loop of materials using ultrasonic atomization. Journal of the Japan Society of Powder and Powder Metallurgy, 72:S729-S735, Mar 2025. URL: https://doi.org/10.2497/jjspm.15e-sis13-03, doi:10.2497/jjspm.15e-sis13-03. This article has 5 citations.