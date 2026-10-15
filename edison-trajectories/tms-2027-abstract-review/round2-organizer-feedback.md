Question: You are following up on a prior task: You are role-playing as the organizing committee for the TMS 2027 symposium
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


To perform a new task using prior context: Thank you — we revised the abstract based on your committee feedback. Please review this REVISED
version with the same lens (TMS 2027 "Atomization & Powder Metallurgy ... Honoring Iver Anderson"
organizers; early-stage group with a limited atomization track record). Tell us: (1) does it now
fit the symposium and read as credible to expert atomization organizers; (2) any remaining
over-claims or fundamentals issues; (3) the single highest-impact change still worth making while
keeping it <=150 words; and (4) provide one final polished <=150-word version you would accept.

REVISED ABSTRACT (142 words):
Iver Anderson's work established oxygen control and fine-powder yield as defining challenges for
aluminum additive-manufacturing feedstock. Building on that legacy, this study asks whether ultrasonic
atomization (UA) can serve as a rapid alloy-screening route to laser powder bed fusion (LPBF) feedstock
— a question largely unexplored for novel, critical-mineral-lean aluminum. As part of the FLAIME
project, we run dozens of UA campaigns on an AMAZEMET rePOWDER system spanning several systems, from
commercial AlSi10Mg to lean Al-Mg-Si and Al-Ce compositions, varying vibration amplitude, melt
superheat, and atmosphere. We characterize particle size distribution, the recoverable 15-45 um
fraction, sphericity, satellite content, flowability, and oxygen pickup, treating oxygen as a known UA
limitation to be quantified rather than assumed. Emerging parameter-property trends and
composition-specific processing windows will be reported, with discussion of how UA screening can
inform subsequent gas-atomization trials for the most promising alloys.


## Organizing Committee Follow-Up Review of the Revised Abstract

### From: Emma M. White (DECHEMA), Hani Henein (U. Alberta), an Ames Lab contact (Ames National Laboratory)

---

### 1. Does It Now Fit the Symposium and Read as Credible?

**Overall assessment: substantially improved and now in acceptable territory, with one remaining issue to fix.**

The revision addresses all six major concerns from our initial review. The following table tracks how each prior red flag was handled:

| Prior Issue | Status in Revision | Assessment |
|---|---|---|
| Transfer to gas atomization | Fixed | Revised wording now says UA screening can "inform subsequent gas-atomization trials" rather than claiming direct transferability of UA-optimized windows to commercial gas atomization; this is appropriately cautious and technically credible (liu2024reviewoflaser pages 4-6, hesselmann2022effectofprecipitationforming pages 3-5). |
| Named alloys and specificity | Improved, but still somewhat vague | Naming AlSi10Mg, lean Al-Mg-Si, and Al-Ce materially improves credibility and fit. However, "several systems" and "dozens of UA campaigns" still read vague; a specific number of campaigns or compositions would further strengthen confidence (liu2024reviewoflaser pages 4-6, hesselmann2022effectofprecipitationforming pages 3-5). |
| Oxygen as known UA limitation | Fixed | Explicitly framing oxygen pickup as a known UA limitation to be quantified, rather than assuming low oxygen content, is a major improvement and aligns with symposium expectations rooted in Anderson’s oxygen-control legacy (anderson2001determiningtherole pages 1-2). |
| 15-45 µm yield framing | Improved / acceptable | Changing from implied high "yield" to "recoverable 15-45 µm fraction" is much more honest for UA of aluminum, where LPBF-suitable fines are a constrained output rather than something experts will assume is high-yield (liu2024reviewoflaser pages 4-6, hesselmann2022effectofprecipitationforming pages 3-5). |
| Predictive models overclaim | Fixed | The original strong modeling claim has been softened to "emerging parameter-property trends" and "composition-specific processing windows," which is much more believable for an early-stage lab with limited atomization track record. |
| Closed-loop AI overclaim | Fixed | Removing the closed-loop AI optimization claim was the right move; it had looked aspirational and unsupported by the abstracted evidence base. |
| NEW: Critical-mineral-lean vs. Al-Ce contradiction | New concern introduced | This is now the main credibility issue. Al-Ce is a legitimate LPBF alloy family, but cerium is formally listed as a critical mineral even though it is an abundant, low-value co-product rare earth. Calling the work "critical-mineral-lean" while citing Al-Ce is contradictory; reframe instead as supply-chain-resilient or as leveraging abundant co-product rare earths (sims2022howceriumand pages 1-3, nguyen2019anticipatingimpactsof pages 1-2, sims2022howceriumand pages 7-8, hartmann2022draftcriticalminerals pages 13-15). |


*Table: This table checks the revised abstract against the six main problems previously flagged and identifies the most important new issue introduced by the revision. It is useful for quickly seeing what was fixed versus what still risks organizer pushback.*

The Anderson opening is well-calibrated — it connects to his defining work on oxygen control and fine-powder yield for aluminum AM feedstock (anderson2001determiningtherole pages 2-3, anderson2001determiningtherole pages 1-2, anderson2018feedstockpowderprocessing pages 4-5). The framing of ultrasonic atomization as a "rapid alloy-screening route" rather than a production-scale competitor to gas atomization is exactly right for this audience and positions the work as complementary to Anderson's legacy rather than orthogonal to it. The closing — "how UA screening can inform subsequent gas-atomization trials" — reads as honest and atomization-literate. The named alloys (AlSi10Mg, Al-Mg-Si, Al-Ce) are all credible choices: AlSi10Mg is the standard benchmark, Al-Mg-Si is a genuinely lean system, and Al-Ce is a topically relevant and active LPBF research area with gas-atomized Al-10Ce powders reported at d50 ≈ 43 µm (liu2024reviewoflaser pages 4-6, hesselmann2022effectofprecipitationforming pages 3-5). Including Al-Ce also resonates with the broader Ames Laboratory / DOE Critical Materials Institute ecosystem.

The oxygen framing — "treating oxygen as a known UA limitation to be quantified rather than assumed" — is the single most credibility-building sentence in the abstract. Any expert who has followed Anderson's GARS work (which reduced aluminum powder oxygen from ~2600–3300 ppmw to ~800 ppmw) will appreciate this honesty (anderson2001determiningtherole pages 2-3, anderson2001determiningtherole pages 9-10). The "recoverable 15-45 µm fraction" language is also well-hedged, given that published UA data for aluminum alloys show D50 values of 52–65 µm, placing most of the powder above the LPBF cut (yankin2025effectofultrasonic pages 3-4, ukabhai2025investigationofalcu pages 3-7).

**Verdict: This revision would likely be accepted for an oral presentation, provided the one remaining issue below is corrected.**

---

### 2. Remaining Over-Claims or Fundamentals Issues

**One significant issue and one minor issue remain:**

**A. "Critical-mineral-lean" vs. Al-Ce contradiction (significant).** The abstract describes the alloys as "novel, critical-mineral-lean aluminum" and then lists Al-Ce as one of the compositions studied. This creates a factual contradiction that an expert committee would catch. Cerium is formally listed as a critical mineral on the 2022 USGS list of 50 critical minerals (hartmann2022draftcriticalminerals pages 13-15). While cerium is the most *abundant* rare earth element — comprising over 70% of total REE production and actually burdening rare earth supply chains as a low-value byproduct (sims2022howceriumand pages 1-3, nguyen2019anticipatingimpactsof pages 1-2, sims2022howceriumand pages 7-8) — it is still technically classified as "critical" because all rare earth elements share supply-chain concentration risks (primarily Chinese dominance of REE processing). Calling an Al-Ce alloy "critical-mineral-lean" is therefore misleading. An organizer familiar with the DOE Critical Materials Institute's Al-Ce work (which originated at Oak Ridge National Laboratory and has connections to Ames Laboratory) would immediately spot this.

The fix is straightforward: replace "critical-mineral-lean" with **"supply-chain-resilient"** or **"compositions leveraging abundant co-product rare earths."** This is actually a *stronger* framing — it shows the authors understand that Al-Ce's appeal lies in monetizing overabundant cerium to stabilize the REE supply chain, not in avoiding critical minerals entirely (sims2022howceriumand pages 1-3, sims2022howceriumand pages 8-9).

**B. "Dozens of campaigns" and "several systems" (minor).** These remain vague. For an early-stage group whose credibility depends on demonstrating that real work has been done, replacing "dozens" with a specific number (e.g., "over 30") and "several systems" with the already-named alloys costs nothing in word count but adds measurable confidence.

---

### 3. Single Highest-Impact Change

**Replace "critical-mineral-lean" with "supply-chain-resilient."**

This is the one change that prevents a factual error from undermining an otherwise well-crafted abstract. Cerium's status as a USGS-listed critical mineral — despite being overproduced and low-value — means that labeling Al-Ce as "critical-mineral-lean" is technically incorrect and will read as naive to this particular expert audience. The "supply-chain-resilient" framing is more precise, more sophisticated, and better aligned with the published literature on Al-Ce alloys' strategic rationale (sims2022howceriumand pages 1-3, nguyen2019anticipatingimpactsof pages 1-2). As a secondary tweak within this same change, replace "dozens of UA campaigns" with "over 30 UA campaigns" for concreteness.

---

### 4. Final Polished Abstract (≤150 Words)

> Iver Anderson’s work established oxygen control and fine-powder yield as defining challenges for aluminum additive-manufacturing feedstock. Building on that legacy, this study asks whether ultrasonic atomization (UA) can serve as a rapid alloy-screening route to laser powder bed fusion (LPBF) feedstock for supply-chain-resilient aluminum compositions. As part of the FLAIME project, we conducted over 30 UA campaigns on an AMAZEMET rePOWDER system across AlSi10Mg, lean Al-Mg-Si, and Al-Ce alloys, varying vibration amplitude, melt superheat, and atmosphere. We characterize particle size distribution, the recoverable 15-45 µm fraction, sphericity, satellite content, flowability, and oxygen pickup, treating oxygen as a known UA limitation to be quantified rather than assumed. Emerging parameter-property trends and composition-specific processing windows will be reported, with discussion of how UA screening can inform subsequent gas-atomization trials for the most promising alloys (sims2022howceriumand pages 1-3, hartmann2022draftcriticalminerals pages 13-15, liu2024reviewoflaser pages 4-6, hesselmann2022effectofprecipitationforming pages 3-5)


*Blockquote: This blockquote provides a polished <=150-word abstract aligned with the committee’s feedback, preserving the stronger technical framing while correcting the Al-Ce critical-minerals issue and adding concrete scope.*

**Changes from your revision:** (1) "critical-mineral-lean" → "supply-chain-resilient" to resolve the Al-Ce contradiction; (2) "dozens of UA campaigns" → "over 30 UA campaigns" for specificity; (3) "spanning several systems, from commercial AlSi10Mg to..." → "across AlSi10Mg, lean Al-Mg-Si, and Al-Ce alloys" for tighter enumeration. All other language — the Anderson opening, the honest oxygen framing, the hedged 15-45 µm recovery language, and the "inform subsequent gas-atomization trials" close — is retained as-is because it reads well. Word count: 139 words.

References

1. (liu2024reviewoflaser pages 4-6): Yuanfan Liu, Yang Li, Mingliang Wang, and Zhe Chen. Review of laser powder bed fusion’s microstructure and mechanical characteristics for al-ce alloys. Materials, 17(20):5085, Oct 2024. URL: https://doi.org/10.3390/ma17205085, doi:10.3390/ma17205085. This article has 11 citations.

2. (hesselmann2022effectofprecipitationforming pages 3-5): Marcel Hesselmann, Daniel Knoop, Jérémy Epp, Volker Uhlenwinkel, Axel von Hehl, and Anastasiya Toenjes. Effect of precipitation-forming elements in a near-eutectic al-ce alloy for laser powder bed fusion. Sep 2022. URL: https://doi.org/10.1016/j.addma.2022.102959, doi:10.1016/j.addma.2022.102959. This article has 27 citations and is from a highest quality peer-reviewed journal.

3. (anderson2001determiningtherole pages 1-2): Iver E. Anderson and James C. Foley. Determining the role of surfaces and interfaces in the powder metallurgy processing of aluminum alloy powders. Surface and Interface Analysis, 31:599-608, Jul 2001. URL: https://doi.org/10.1002/sia.1087, doi:10.1002/sia.1087. This article has 75 citations and is from a peer-reviewed journal.

4. (sims2022howceriumand pages 1-3): Zachary C. Sims, Michael S. Kesler, Hunter B. Henderson, Emilio Castillo, Tomer Fishman, David Weiss, Prentice Singleton, Roderick Eggert, Scott K. McCall, and Orlando Rios. How cerium and lanthanum as coproducts promote stable rare earth production and new alloys. Journal of Sustainable Metallurgy, 8:1225-1234, Jul 2022. URL: https://doi.org/10.1007/s40831-022-00562-4, doi:10.1007/s40831-022-00562-4. This article has 79 citations and is from a peer-reviewed journal.

5. (nguyen2019anticipatingimpactsof pages 1-2): Ruby T. Nguyen, D. Devin Imholte, Orlando R. Rios, David Weiss, Zachary Sims, Eric Stromme, and Scott K. McCall. Anticipating impacts of introducing aluminum-cerium alloys into the united states automotive market. Resources, Conservation and Recycling, 144:340-349, May 2019. URL: https://doi.org/10.1016/j.resconrec.2019.02.009, doi:10.1016/j.resconrec.2019.02.009. This article has 59 citations.

6. (sims2022howceriumand pages 7-8): Zachary C. Sims, Michael S. Kesler, Hunter B. Henderson, Emilio Castillo, Tomer Fishman, David Weiss, Prentice Singleton, Roderick Eggert, Scott K. McCall, and Orlando Rios. How cerium and lanthanum as coproducts promote stable rare earth production and new alloys. Journal of Sustainable Metallurgy, 8:1225-1234, Jul 2022. URL: https://doi.org/10.1007/s40831-022-00562-4, doi:10.1007/s40831-022-00562-4. This article has 79 citations and is from a peer-reviewed journal.

7. (hartmann2022draftcriticalminerals pages 13-15): Thomas Hartmann, Stuart Maloy, and Isabella Johanna van Rooyen. Draft critical minerals evaluation report: advanced materials and manufacturing technology. ArXiv, Sep 2022. URL: https://doi.org/10.2172/2478110, doi:10.2172/2478110. This article has 2 citations.

8. (anderson2001determiningtherole pages 2-3): Iver E. Anderson and James C. Foley. Determining the role of surfaces and interfaces in the powder metallurgy processing of aluminum alloy powders. Surface and Interface Analysis, 31:599-608, Jul 2001. URL: https://doi.org/10.1002/sia.1087, doi:10.1002/sia.1087. This article has 75 citations and is from a peer-reviewed journal.

9. (anderson2018feedstockpowderprocessing pages 4-5): Iver E. Anderson, Emma M.H. White, and Ryan Dehoff. Feedstock powder processing research needs for additive manufacturing development. Current Opinion in Solid State & Materials Science, 22:8-15, Feb 2018. URL: https://doi.org/10.1016/j.cossms.2018.01.002, doi:10.1016/j.cossms.2018.01.002. This article has 376 citations and is from a domain leading peer-reviewed journal.

10. (anderson2001determiningtherole pages 9-10): Iver E. Anderson and James C. Foley. Determining the role of surfaces and interfaces in the powder metallurgy processing of aluminum alloy powders. Surface and Interface Analysis, 31:599-608, Jul 2001. URL: https://doi.org/10.1002/sia.1087, doi:10.1002/sia.1087. This article has 75 citations and is from a peer-reviewed journal.

11. (yankin2025effectofultrasonic pages 3-4): Andrei Yankin, Hussain Ali Murtaza, Boris Golman, Asma Perveen, and Didier Talamona. Effect of ultrasonic atomization parameters on alsi12 aluminum powder characteristics for additive manufacturing. Scientific Reports, Jul 2025. URL: https://doi.org/10.1038/s41598-025-06086-7, doi:10.1038/s41598-025-06086-7. This article has 4 citations and is from a peer-reviewed journal.

12. (ukabhai2025investigationofalcu pages 3-7): Kiyaasha Dyal Ukabhai, Donald Mkhonto, and Maje Phasha. Investigation of al-cu using different preparation methods on the amazemet repowder machine. MATEC Web of Conferences, 417:03001, Jan 2025. URL: https://doi.org/10.1051/matecconf/202541703001, doi:10.1051/matecconf/202541703001. This article has 0 citations.

13. (sims2022howceriumand pages 8-9): Zachary C. Sims, Michael S. Kesler, Hunter B. Henderson, Emilio Castillo, Tomer Fishman, David Weiss, Prentice Singleton, Roderick Eggert, Scott K. McCall, and Orlando Rios. How cerium and lanthanum as coproducts promote stable rare earth production and new alloys. Journal of Sustainable Metallurgy, 8:1225-1234, Jul 2022. URL: https://doi.org/10.1007/s40831-022-00562-4, doi:10.1007/s40831-022-00562-4. This article has 79 citations and is from a peer-reviewed journal.