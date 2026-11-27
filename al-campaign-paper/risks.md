# What makes the main claim hard to support by Feb 28, 2027

*Status of 2026-11-27. Evidence links are to issues, PRs and branches in this repo. Owners are proposals; change them
in [`figure-plan.csv`](figure-plan.csv) and here.*

The claim: **a scandium-free alloy, printed by LPBF from powder made in-house, stronger than AlSi10Mg and with less
critical minerals than Scalmalloy.** Fourteen things stand in the way. The first two are about what the claim means and
cost nothing to fix but a decision. The rest are about getting the data in time.

## The two decisions that shape the paper (decide by Tue Dec 1, before the screen ranks anything)

### R1. "Stronger than AlSi10Mg without scandium" is already published, and already for sale

On vendor datasheets, directly aged Al-Mn-Cr-Zr (Höganäs Al-HS1, 355-370 MPa yield) and Al-Mg-Zr-Mn (EOS
Al5X1, 380-385 MPa) are well above as-built AlSi10Mg (233-300 MPa). Aged Al-Fe-Zr (Aheadd CP1, about 300 MPa) matches its
top end. Peer-reviewed Al-Mn-Cr-Zr-Mg (390 MPa as built), Al-Mg-Zr (350-353 MPa aged) and Al-Mg-Mn-Er-Zr (440 MPa aged)
are in the same range or above (Fig. 1a; [`data/literature-alloys.csv`](data/literature-alloys.csv); sources in the
[#275 survey](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/claude/issue-275-20261126-0632/bofn-seeding/first-six/research/datasheets.md)).
All four Sc-free #275 seeds and all three optional ones are published alloys (S4 from an abstract only), and S1, S2,
S3, O1 and O2 are the ones plotted here.

- **Effect on the paper:** making S1 in-house and showing that it beats AlSi10Mg is a replication, not a discovery. A
  reviewer at *Scripta* or *MRL* will say so.
- **What would count as new:**
  - (a) a composition that sits beyond the existing Sc-free alloys on strength against burden (Fig. 1b);
  - (b) the same strength from fewer or less critical additions;
  - (c) a result about the route itself, which belongs to #120 (see R12).
- **Decision (Sterling, with Xavier):** set the campaign's objective as "beyond the Sc-free front", not "beyond
  AlSi10Mg", and keep the literature alloys as seeds only to anchor the model.

### R2. The burden metric decides the claim

Every alloying element in play except iron is on the final 2025 U.S. list, and so are aluminum and silicon themselves
([Federal Register 2025-19813](https://www.govinfo.gov/content/pkg/FR-2025-11-07/html/2025-19813.htm)). So "less
critical minerals" needs a weighted metric. [`scripts/mineral_burden.py`](scripts/mineral_burden.py) computes two from
USGS *Mineral Commodity Summaries 2026* inputs ([`data/element-criticality.csv`](data/element-criticality.csv)), and they
disagree:

| Alloy | B_NIR, import-weighted (wt %) | B_cost, critical additions (USD/kg alloy) |
|---|---|---|
| AlSi10Mg | 5.2-10.3 | 0.31 |
| Scalmalloy | 4.7-6.0 | 39.9 |
| S1 Al-Mn-Cr-Zr-Mg (planned seed) | 6.6-7.3 | 0.62 |
| S2 Al-Fe-Mg-Zr (planned seed) | 0.9-1.6 | 0.31 |
| S3 Al-Si-Mg (planned seed) | 3.6-6.0 | 0.28 |
| S4 Al-Mg-Si-Ti (planned seed) | 6.5-9.2 | 0.58 |
| O1 Al-Mg-Zr (optional seed) | 2.9-4.2 | 0.53 |

Some import reliances come only as bounds (Si > 50 %, Mg > 75 %, Zr < 25 %), so B_NIR is an interval.

- **Import-weighted mass:** at the midpoints AlSi10Mg scores above Scalmalloy because of its 10 wt% Si; the intervals
  overlap. Most of Scalmalloy's burden is its Mg, not its Sc. The Mn-rich S1 scores above Scalmalloy's whole
  interval. The premise from the kickoff (08:47), that only Scalmalloy uses critical minerals, doesn't clearly hold
  on this measure.
- **Cost:** with Sc priced as metal, every Sc-free alloy is at least 97 % below Scalmalloy, apart from the two
  silver-bearing Al-Cu-Mg grades (74-87 % below). Priced through an Al-2Sc master alloy, the floor is 92 % for the
  silver-free alloys but only 14-56 % for the silver-bearing ones, so A20X would fail FLAIME's 40 % threshold. For
  silver-free alloys the condition is met almost automatically and the claim rests on strength.
- **Decision (Sterling):** pick the primary metric and the threshold before the screen ranks anything, and commit it
  (S9 in the SI). Under B_NIR, steer toward Fe-, Zr- and Mg-lean families (S2, O1) and away from Mn-rich ones (S1, O3).
  Under B_cost, say plainly that any Sc-free alloy passes.
- **Inputs to check by hand:**
  - The Mn price is the 2023 Minerals Yearbook value, because MCS 2026 prices only ore.
  - Ce, Er and V are priced on an oxide basis.
  - No Graedel or Helbig element scores were accessible. The PNAS SI sits behind a reCAPTCHA, and someone with a
    browser can download it.

## Getting the data in time

| # | Risk | Evidence | What it does to the claim | Do now | Owner | By |
|---|---|---|---|---|---|---|
| R3 | **No Al powder has been made yet, and the atomizer is down** | No run since the Nov 13 bronze run burned the collection cup ([#269](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/269)). AMAZEMET's glass cup "will take some"; no restart date. The five Al runs of Oct 2-22 made "little or no powder" ([PR #288](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/288), [#286](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/286)) | Block A (Nov 17-24) didn't happen. If the first good Al run slips past mid-December, version A can't be done by Feb 28 | Check today whether the "spare glass and spare seals" from the spares kit (training video 9) exist. If not, build the lab cup's fastest option (catalogue KF-50 parts, about $200 at list price, #269). Merge the SOP (#253) | Gage | Dec 4 |
| R4 | **No LPBF session is booked** | Last Utah MIDI contact Oct 7 ([#138](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/138#issuecomment-6353376533)). April's turnaround was about 11 days. A desktop machine can't print Al before late Dec to Feb even if approved now ([PR #294](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/294)) | Without prints there is no "printable" and no tensile | Book P2 (mid-Dec), P3-P4 (Jan) and P5 (early Feb) at Utah. Ask for the 55 mm reduced build platform and the April build's laser parameters | Carl, Ronnie | Dec 11 |
| R5 | **Too little powder for a build** | A 250 g charge gives about half its mass below 63 µm at best (#275's estimate); a full MIDI build needs about 440 g ([#138](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/138#issuecomment-6353376533)) | Tensile bars may only be possible for 1-2 alloys, and only with the reduced platform | Confirm the reduced platform (about 30 g). Plan two to three runs per finalist | Carl, Gage | Dec 11 |
| R6 | **Feedstock for most seeds isn't ordered** | Zr, Fe, Ni, Cu and Si powder aren't on any order; no master alloys bought ([#146](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/146#issuecomment-6842840090), [#250](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/250#issuecomment-6778615370)). Zr alloys need 1040-1060 °C melts, untried on this machine (#275) | S1, S2, O1, O2 and the Scalmalloy-type D2 can't be made | Order Al-10Zr master alloy and Fe now. Run D1, S3, S4 and O3 first ([#275](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/275)) | Gage | Dec 4 |
| R7 | **The CALPHAD screen can't yet do what the methods say** | No Thermo-Calc licence; #141 unanswered. The open MatCalc database has no Al₃Zr liquidus. The seeds come from the literature, not the screen ([#275 branch](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/claude/issue-275-20261126-0632/bofn-seeding/first-six/README.md)) | "Thermo-Calc screening" in the title of a method section would overstate it, and Zr alloys can't be ranked | Decide the licence. If none, say "pycalphad with open databases" and check the finalists in Thermo-Calc through a partner | Xavier, Sterling | Dec 4 |
| R8 | **Composition can't be verified yet** | EDS is good to 0.2-0.5 wt % at best (kickoff 10:36-11:29); standards-based EDS has one valid run ([PR #288](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/288)). ICP for Si needs HF digestion. No outside lab contacted | "Composition confirmed by an outside lab" can't be written | Contract an outside lab now. Spark-OES on a printed coupon (ASTM E1251) avoids dissolving Si. Ship batch 1 by Jan 8, finalists by Jan 29 | Sterling | Dec 18 |
| R9 | **Tensile set-up** | The 20 kip frame was last reported broken. April's yields for tests 1-3 are unreliable: their elastic slopes were 29-49 GPa, against about 70 GPa for Al. No extensometer is recorded ([PR #288](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/288)) | The in-house AlSi10Mg bar (228 ± 13 MPa) is provisional | Get an extensometer or DIC. Re-test commercial and in-house AlSi10Mg in the finalists' build | Carl | Jan 15 |
| R10 | **No density or hardness set-up** | Archimedes (#144) idle since June; nothing exists ([#284](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/284#issuecomment-7175752102)). Microhardness access unconfirmed | Hardness is the optimizer's fast screen. Without it, no optimizer rounds | Set up Archimedes (Seth offered in June) and book the microhardness tester | Carl | Dec 18 |
| R11 | **Corrosion isn't ready** | The EZstat-Pro has passed dummy-cell checks only. One reference electrode is on order. The CubXL cell is unbuilt and copper goes first ([PR #239](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/239), [PR #264](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/264)) | Fig. 6 and the corrosion results | Validate on a reference by Jan 15, or move corrosion to future work (the schedule's first cut) | Ben, Jarrett | Jan 15 |
| R12 | **Overlap with the *Adv. Mater.* article** | #120 says the atomization results are "saved" for it, and a run on #120 started today. [`outline.md`](outline.md#keeping-this-paper-apart-from-the-advanced-materials-article-120) proposes a split | A journal checks prior publication. Two papers built on the same runs need different claims | Decide the split | Sterling | Dec 4 |
| R13 | **Too few people** | One run takes 10-15 person-hours from charge to SEM. Only Gage, Ronnie and Sterling may run the atomizer (#160), and no third operator or new SEM users are in training | 3-4 runs a week can't be sustained | Train a third operator and two SEM users | Gage, Sterling | Dec 18 |
| R14 | **Independent verification** | No outside lab contacted, and "we have some contacts" (kickoff 11:41) aren't named anywhere | Outside tensile by Feb 28 isn't realistic; outside chemistry is, if contracted by mid-December | Contract chemistry now (R8). Leave outside tensile for revision | Sterling | Dec 18 |

## What fits in each version

- **Version A (a new alloy, Feb 28):** all of R3-R10 resolved by mid-December, plus a good Al run before the break.
  Given where things stand, I put this below one in five.
- **Version B (a benchmarked screen):** needs a good Al run by about Dec 18 and at least two Utah sessions in January.
  It is realistic for **late March 2027**.
- **Version C (no new experiments):** the benchmark and burden analysis in §4 of the draft is already a short paper.
  It covers what "less critical" means for LPBF Al alloys, AlSi10Mg printed and tested in-house against the
  datasheets, and where the Sc-free commercial and published alloys sit. It can be submitted by Feb 28 whatever
  happens to the atomizer, but it is not the discovery the campaign is after. It would also pre-empt part of
  versions A and B, so decide this before writing it up.

## What the first good Al run date buys

The critical path is: a good Al run, the seeds, a Utah session for cubes, a pick of finalists, finalist powder, a Utah
session for tensile bars, heat treatment and testing, and outside chemistry (2-3 weeks). It assumes the
[#256 schedule](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/claude/issue-256-20261112-2149/al-campaign-schedule/README.md)'s
post-break weeks and that R4-R10 are fixed in time. These are judgments, not a computed schedule.

| First Al run that makes LPBF-grade powder | Seeds made | Finalists' tensile | Version A submitted | Version B submitted |
|---|---|---|---|---|
| By Fri Dec 11 | S3, S4, O3 before the break; Zr seeds early January | Feb 9-12 (P5 on Feb 2-3) | Feb 28 possible but unlikely: everything else has to go right | Feb 28 |
| Dec 14-18 | January | late February | about mid-April | about Mar 31 |
| After the break (Jan 4 or later) | mid-January to early February | March | May-June | about Apr 30 |

"LPBF-grade" means at least about 100 g below 63 µm from one charge. None of the five Al runs so far came close
(R3).

## Cut order if behind (from the schedule, adjusted)

1. Corrosion beyond the finalists (or all of it, if R11 isn't fixed by Jan 15).
2. Optimizer round R4.
3. DED (nothing is booked, and no Al DED has been discussed).
4. Block A and the B dosing checks: under the proposed split they belong to #120 anyway.

**Never cut:** the in-house AlSi10Mg comparator in the finalists' build, ≥ 3 valid tensile specimens per finalist, the
outside composition check, and the frozen metric.
