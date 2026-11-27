# Results each section needs, and who supplies them

*Draft of 2026-11-27. One row per result. "Status" is what exists today, from the run table (PR #286), the
campaign threads (#256, #277), the printing and twin threads (#260, #276) and the optimizer benchmarks
(`bofn-prelim`, PR #297). "Owner" is the person or project that has to produce it. People are named by
first name as in the threads; the author list itself is decision D4 in the [README](README.md).*

Suppliers:
- **Campaign 1**: Nov 2026–Feb 2027, 36 Al + 4 Cu atomizer runs (#256, #277). Its alloys belong to the
  campaign paper; this article uses its atomizer runs, logs and costs, and its data as prior data.
- **Blocks A/B**: the atomizer runs plan (byu-vcl `atomizer-runs/plan-adv-mater/` @ `cad4e6d`): A = repeats at
  fixed settings, B = the 4047-in-6063 composition spread. Planned inside campaign 1.
- **Campaign 2**: the 2027 campaign run by the cost-aware optimizer with the desktop LPBF in the loop.
  Not yet planned anywhere; [`timeline.md`](timeline.md) proposes dates.
- **Desktop LPBF**: #260 (design in PR #266, fast-track options in PR #294, monitoring in PR #281).
- **Twin**: #276 (byu-vcl PRs 393–394; audit PR #293).
- **CALIBER**: the lab's composition and microstructure measurement work.
- **Outside lab**: composition (ICP-OES, O/N/H by inert-gas fusion) and, if funded, tensile.

## §2.1 The loop and its costs (Fig. 1, Table 1)

| ID | Result | Supplied by | Status (Nov 27) | Owner | Due |
|---|---|---|---|---|---|
| L1 | Person-hours and machine-hours for every step of every run, print and test, logged at the bench with timestamps | campaigns 1 and 2 | **none**: nothing timed end to end; #256's 10–15 person-h per run is an estimate | each station lead: Gage (atomizer), Ronnie (powder, SEM), Carl (printing), Xavier (CALPHAD, optimizer) | start now; final Nov 2027 |
| L2 | Consumables and $ per step (plates, nozzles, crucibles, BN, argon, powder, outside fees) | campaigns 1 and 2 | **partial**: argon 100–160 psi per Al run; a Mo plate lasts 4–6 runs, W-coated plates are single-use (#219) | Gage, Carl | Mar 2027; final Nov 2027 |
| L3 | Calendar time from composition to a measured cube, in-house vs. outside build | campaign 2 | **none** | Gage | Oct 2027 |

## §2.2 Making powder (Fig. 2, SI S1–S9)

| ID | Result | Supplied by | Status (Nov 27) | Owner | Due |
|---|---|---|---|---|---|
| A1 | ≥ 5 valid Block A runs (6063, 250 g, Mo plate, 1.5:1, amplitude 90), each with a filled run record (YAML template) | Block A | **none**. Scheduled Nov 17–24; blocked since the collection cup failed on Nov 13 (#269). Also waiting on: Mo plates, the 45 µm sieve, one lot of 6063 | Gage, Ronnie | **Mar 2027** |
| A2 | Their PSDs (two splits each; sieve fractions at 250/63/45 µm; SEM sizing ≥ 1,000 particles), circularity (≥ 400), six-part mass balance | Block A | **none** for Al. One SEM PSD exists, for the bronze lot k7m2q9 (PR #226), and the bronze runs' pooled mass balance (52.4 % usable) | Ronnie | Mar 2027 |
| A3 | Every run's settings and outcome, failed runs included, for the process window | campaigns 1 and 2 | **partial**: 10 runs Oct 2–Nov 13 (PR #286); no Al powder weighed; HMI export never set up (settings read from video) | Gage | ongoing |
| A4 | Runs varying superheat and amplitude, only if Block A shows they matter (#111) | campaign 1 flex slots or 2027 | **none** | Sterling decides; Gage runs | Jun 2027 |
| A5 | Powder O/N on sealed 5 g samples by inert-gas fusion | outside lab | **none**; samples not yet kept | Sterling (vendor, funding); Gage keeps samples | Jun 2027 |
| A6 | Re-check that no fixed-setting repeatability study of ultrasonic atomization of Al has appeared (Oct 2026 check found one replicate study for any alloy: Hinrichs 2021) | literature | done Oct 7, 2026. Re-checked one candidate on Nov 27: Yankin 2025 (*Sci. Rep.* 15, 20524; AlSi12, arc-melting atomizer) is a parameter study; its D50 of 52.3–54.7 µm spans different settings, not replicate runs, so the runs plan's "Yankin D50 ±2 %" is not a repeatability figure | a Claude run | Oct 2027 and Jan 2028 |

## §2.3 Composition fidelity (Fig. 3)

| ID | Result | Supplied by | Status (Nov 27) | Owner | Due |
|---|---|---|---|---|---|
| C1 | Charge composition as weighed vs. target, every charge | campaigns 1 and 2 (dosing logs) | **none** for charges | Gage, Paul (cups and bar) | Mar 2027 |
| C2 | Block B spread (B1–B7: 22.5, 7.5, 30, 0, 15, 30, 7.5 wt% 4047 → ~1.3–3.9 wt% Si): EDS per particle at top/middle/bottom of the jar, plus ICP-OES | Block B + outside lab | **none**; Oct 2 (u23y78) is a pilot point | Gage (runs), Ronnie (EDS), Sterling (ICP) | Jun 2027 |
| C3 | Mg recovery through atomization and through printing (ICP on charge, powder, print) | campaigns 1–2 + outside lab | **none** | Ronnie, Sterling | Sep 2027 |
| C4 | EDS against ICP for Si-free and Si-bearing alloys: bias and precision, for the composition node's noise model | CALIBER + outside lab | **partial**: standards-based EDS on the Utah AlSi10Mg coupon (PR #288), only 1 of 17 EDS runs valid; the kickoff raised 0.2–0.5 wt% EDS error for Si | Ronnie (CALIBER) | Jun 2027 |

## §2.4 Printing in-house (Fig. 4)

| ID | Result | Supplied by | Status (Nov 27) | Owner | Due |
|---|---|---|---|---|---|
| P1 | A desktop LPBF system printing Al cubes: commissioned, O₂ logged, laser power calibrated | desktop LPBF | **none**: design only; no build-or-buy decision; nothing ordered; laser safety and EHS not yet asked. FT-1 (PR #294) estimates 3.7–9.3 weeks from order to first coupons, plus approvals | Sterling (decision, approvals); Carl (build) | **May 2027** for version A |
| P2 | Single tracks and cubes of campaign 2 powders: power–speed maps, density, cracking, monitoring signals | desktop LPBF | **none**; no single tracks have been measured on any machine | Carl | Aug 2027 |
| P3 | The same powders printed on the Utah Aconity MIDI (reference) | Utah (Spear lab) | **partial**: one AlSi10Mg build from commercial powder (Apr 2026). A full cylinder needs ~440 g; the Ø55 mm kit (~30 g) may not exist at Utah. Sessions P1–P5 proposed, not booked | Carl | Sep 2027 |
| P4 | Archimedes density and hardness on every print; desktop vs Utah parity | campaigns 1–2 | **none**; density set-up scheduled for Dec 4 (#144) | Carl, Ronnie | Sep 2027 |
| P5 | Metallography of cracking against the CALPHAD crack index | campaigns 1–2 | **none** | Ronnie, Xavier | Oct 2027 |

## §2.5 The optimizer chooses the step (Fig. 5, Table 2)

| ID | Result | Supplied by | Status (Nov 27) | Owner | Due |
|---|---|---|---|---|---|
| B1 | The optimizer running live on the real nodes, with measured costs, failure handling (#274), seeding (#275), and the pre-registered baselines, targets and stopping rule | optimizer code | **partial**: synthetic benchmarks only. Open problems: pKGFN's knowledge gradient is zero for most candidates on 64–71 % of decisions (PR #297) and for 73 % of tensile tests at κ = 0; the GP-network port fails on BoTorch 0.18.1 (#274); multi-output nodes (#91, #104) | Xavier, Sterling (with Claude runs) | pre-register by **Jun 2027** |
| B2 | The decision log: every acquisition, with its value, cost and the step chosen | campaign 2 | **none** | Xavier | Oct 2027 |
| B3 | Campaign 2 itself: ~12 weeks, ~25–35 atomizer runs, desktop printing, hardness and density on all, tensile on finalists | campaign 2 | **not planned yet** | whole team | Jul–Oct 2027 |
| B4 | Mineral burden B = Σ wᵢ·NIRᵢ (USGS MCS 2026) for every alloy, with the campaign paper's definition | script in the campaign paper's folder | **none computed** (defined four ways in the FLAIME proposal; campaign paper proposes this one) | Xavier or a Claude run | Mar 2027 |
| B5 | Finalists: ≥ 3 valid tensile specimens each, and AlSi10Mg printed and tested the same way | campaign 2 + Utah (the desktop plate can't make standard bars) | **partial**: Utah AlSi10Mg n = 4 (YS 228 ± 13 MPa) | Carl | Nov 2027 |

## §2.6 When it pays off (Fig. 6)

| ID | Result | Supplied by | Status (Nov 27) | Owner | Due |
|---|---|---|---|---|---|
| T1 | The twin refit to lab records (failure rate, runs per week, usable powder, tensile scatter, AlSi10Mg yield) and extended with the desktop LPBF | twin | **partial and off**: no simulator fitted to a lab measurement; round-2 audit (PR #293) lists the gaps in figure-plan.md | Sterling (with Claude runs) | Apr 2027 (campaign 1 data); Nov 2027 (campaign 2) |
| T2 | Counterfactual campaigns: ≥ 20 seeds per policy and condition, matched-seed bootstrap CIs, baselines fixed in advance | twin | **partial (synthetic)**: bofn-prelim and bofn-clocked | Sterling (with Claude runs) | Dec 2027 |
| T3 | Sensitivity of the gain to screen error κ and to the step-cost ratios | twin | **partial (synthetic)** | same | Dec 2027 |
| T4 | Validation: the twin, given campaign 2's decisions, reproduces its spend and timeline within a stated tolerance | twin + campaign 2 | **none** | same | Dec 2027 |

## Verification (§2.5, Experimental Section)

| ID | Result | Supplied by | Status (Nov 27) | Owner | Due |
|---|---|---|---|---|---|
| V1 | Outside composition (ICP-OES, O/N/H) on the finalists, blind-labelled | outside lab | **none**; no lab chosen | Sterling | Dec 2027 |
| V2 | Outside tensile on the finalists, if funded | outside lab | **none** | Sterling | Dec 2027 |

## Version B needs only

A1–A3, A5, C1–C2, C4, L1–L2, B4, T1–T3, plus campaign 1's data (cited, not re-claimed). Everything for version B
can exist by **Jul 2027** if Block A runs by March, which leaves room to submit it to the collection even if
the desktop LPBF or the live optimizer slips.
