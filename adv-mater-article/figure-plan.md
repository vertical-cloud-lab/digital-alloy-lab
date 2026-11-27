# Figure and table plan

*Draft of 2026-11-27. Six main figures and two tables, about the middle of what recent* Advanced Materials
*closed-loop and AM-alloy papers carry (see [`journal-format.md`](journal-format.md)). Every panel lists what
exists now, what it still needs, which campaign or project supplies it, and when. IDs such as A2 or P3 point
to rows in [`results-needed.md`](results-needed.md). "Campaign 1" is the Nov 2026–Feb 2027 campaign
(#256/#277) whose alloys belong to the campaign paper; "campaign 2" is the 2027 optimizer-driven campaign this
article needs for version A ([`outline.md`](outline.md) §4–5).*

Status key: **have** = data or asset exists; **partial** = some of it; **none** = nothing yet.

## Fig. 1 The loop and what each step costs (§2.1)

| Panel | Content | Status | Needs (IDs) | Supplied by | Due |
|---|---|---|---|---|---|
| a | The workflow as a network, with a photograph of each station: CALPHAD, dosing, atomizer, sieves/SEM, desktop LPBF, metallography, tensile; composition and laser settings as inputs; the optimizer below | **partial**: `figures/al-lpbf-network/al-lpbf-network.png` @ `a68b67d` (branch `claude/issue-284-20261125-2157`, #284) has real images, but the sieve and density tiles are renders, the CALPHAD tile is an Al–Cu–Si Scheil plot, and there is no desktop LPBF yet. Draft schematic: `figures/fig1-loop.tikz` here | photo of each station; desktop LPBF photo (P1) | #284; desktop LPBF (#260) | Aug 2027 |
| b | Cost per result for each step (hours of person time, machine time, consumables, $), log scale, median and range | **none**: no step has been timed end to end (#256 "durations are estimates") | L1, L2 | step-time logs in both campaigns | Mar 2027 (campaign 1), Nov 2027 (final) |
| c | One candidate's path in calendar time, composition to measured cube: in-house (desktop) against an outside build (Utah booking 7 d + return 2 d) | **none** | L3 | campaign 2 logs; twin facility model for the Utah arm | Nov 2027 |

## Fig. 2 Making powder for any composition (§2.2)

| Panel | Content | Status | Needs | Supplied by | Due |
|---|---|---|---|---|---|
| a | From charge to powder: cutaway of cup, plug and dosed core (CAD, byu-vcl PR 232); the machine in section with the landing point (viz3d, PR #173); a good pour (viewport frame); SEM of the 15–45 µm cut | **partial**: CAD and viz3d renders exist; no valid Al pour filmed; no Al SEM sizing | A1 | Block A | Mar 2027 |
| b | Repeatability at fixed settings: cumulative PSDs of every valid Block A run (both splits), D10/D50/D90 against run order with plate changes marked, six-part mass balance as stacked bars | **none**: Block A (6063, 250 g, Mo plate, 1.5:1, amplitude 90) has not run; it was blocked on Nov 13 when the collection cup failed (#269) | A1, A2 | Block A (A1–A5, up to A8) | Mar 2027 |
| c | Each metric's CV against the bar set before A1, beside published spreads (Hinrichs 2021, three replicates: d90 CV ≈ 11 %, O CV ≈ 6 %; Yankin 2025; NIST gas atomization) | **none** | A2, A5 | Block A + outside powder O | Jun 2027 |
| d | Process window across every run, failed ones included: in-range yield and D50 against amplitude, superheat and pour pressure, by plate material | **partial**: 10 runs Oct 2–Nov 13 (5 Al, 5 C63000 bronze) in `atomizer-runs/runs.csv` @ `8320f13` (PR #286); no Al powder weighed; one NAB PSD (k7m2q9: volume D10/D50/D90 = 45.8/103.7/208.5 µm, PR #226) | A3, A4 | every run, both campaigns | Nov 2027 |

SI: **S1** where the melt met the plate (Oct 2 overshoot, Oct 6 sonotrode, Oct 8 frozen lump, Oct 21 wrong position) against a valid run — frames exist (PR #176, `2026-10-21/` @ `5d1cf0c`), needs one valid run; **S2** process logs per run (O₂ through washes, temperature, pour pressure) — HMI export never set up, read from video frames; **S3** mass balance of every run; **S4** variance components (split vs run); **S5** cross-sections (porosity, Mo/W pick-up); **S6** plate wear; **S7** flowability (doser V_g, Hausner) vs commercial AlSi10Mg; **S8** powder O vs chamber O₂ at pour and storage time; **S9** collection-cup failure (#269) and the redesign.

## Fig. 3 Composition fidelity from charge to powder to print (§2.3)

| Panel | Content | Status | Needs | Supplied by | Due |
|---|---|---|---|---|---|
| a | Dosing error per element (target vs weighed charge) | **none** for charges; doser accuracy data in powder-doser repo (see results-needed C1) | C1 | dosing logs, campaign 1 | Mar 2027 |
| b | Si in powder vs Si in charge across the 4047-in-6063 spread (0, 7.5, 15, 22.5, 30 wt% 4047 → from the cup's 0.2–0.6 wt% Si to ~3.4–4.3 wt%), EDS mean (≥ 30 particles) and ICP-OES, 1:1 line, spec range as bars | **none**: Block B not run; Oct 2 u23y78 is a pilot point | C2 | Block B (B1–B7) + outside ICP-OES | Jun 2027 |
| b′ | **The campaign's own additions:** Zr, Sc or Er, and Mn in powder (ICP-OES, by sieve fraction, 15–45 µm cut) against the charge, including Zr dissolution at Al pouring temperatures and any loss to carbides in the graphite crucible. 5 kV EDS can't see the K lines of Mn, Cr, Fe, Ni, Cu, Zn | **none** | C5 | campaigns 1–2 + ICP-OES | Sep 2027 |
| c | Per-particle Si at the top, middle and bottom of the jar; EDS map of a sectioned particle at the 30 wt% point | **none** | C2 | Block B, SEM prep SOP (byu-vcl PR 284) | Jun 2027 |
| d | Mg recovery (ICP ÷ charge) through atomization and printing | **none** | C3 | ICP on powder and on prints | Sep 2027 |
| e | EDS against ICP: bias and precision for Si-free and Si-bearing alloys, which becomes the composition node's noise | **partial**: standards-based EDS on the Utah AlSi10Mg coupon (Mg 0.35 ± 0.01, Si 11.12 ± 0.13 wt%; only 1 of 17 runs valid; PR #288) | C4 | CALIBER + outside ICP | Jun 2027 |

## Fig. 4 Printing in-house (§2.4)

| Panel | Content | Status | Needs | Supplied by | Due |
|---|---|---|---|---|---|
| a | The desktop LPBF system (photo, section, monitoring sensors) | **none**: design only (PR #266; fast-track FT-1 in PR #294); not ordered | P1 | desktop LPBF (#260) | first Al coupons by May 2027 for version A |
| b | Single tracks and cubes from in-house powders: power–speed map with density and cracking, layer-camera and photodiode signals | **none**: no single tracks measured anywhere (#238, #249) | P2 | desktop LPBF + campaign 2 powders | Aug 2027 |
| c | Desktop vs Utah Aconity MIDI on shared powders: density and hardness parity, Spearman ρ, offset. Needs **≥ 8 alloys** (with 5, only a perfect ranking reaches p < 0.05) and matched plate preheat; includes the **route control**, in-house AlSi10Mg printed in the same session as the commercial lot on both machines, and the **industry baselines** (Al5X1, Al-HS1), whose commercial powders anchor both machines to a known alloy and count toward the 8 | **partial**: one Utah AlSi10Mg build from commercial powder (Apr 2026; as-built horizontal YS 228 ± 13 MPa, UTS 376 ± 10, EL 4.5 ± 0.5 %, n = 4; PR #288) | P3, P4 | desktop + Utah sessions on the same powder lots | Sep 2027 |
| d | Cracking against the CALPHAD crack index: Zr/Sc-bearing alloys crack-free despite a high index (the "screen is wrong" evidence that Fig. 6 builds on) | **none** | P5 | campaign 1 + 2 prints, metallography | Oct 2027 |

## Fig. 5 A campaign in which the optimizer chooses the step (§2.5)

| Panel | Content | Status | Needs | Supplied by | Due |
|---|---|---|---|---|---|
| a | Every candidate as a row, the steps it reached, and where and why it stopped, each stop labelled **failure, constraint or acquisition** (acquisition value vs cost at each decision). **The novelty sentence rests on the acquisition stops.** | **none** | B1, B2 | campaign 2 decision log | Oct 2027 |
| b | **Stop audit:** the share of acquisition stops (random 25 % pushed one step further) that would have been worth continuing, i.e. the false-stop rate; plus best-so-far against spend with the twin's replays | **none** | B7, B3, T2 | campaign 2 + twin | Nov 2027 |
| c | **The front to expand.** Aged yield strength against mineral burden B (the metric frozen with the campaign paper, D9). It shows the **industry Sc-free baselines printed and tested here** (EOS Al5X1, Höganäs Al-HS1; filled, 95 % CIs), each joined by a line to its data-sheet value (open); the line shows the parity check. Their front is drawn as a step line, with the region beyond it, and below Scalmalloy's burden (T), shaded. Scalmalloy printed here by the campaign paper is in the front but never binds. Also shown: AlSi10Mg from the same sessions (the floor); every campaign 2 candidate that reached tensile, and campaign 1's best; the **Sc-free front on reported values** (the campaign paper's comparator set) as a dotted staircase, which an alloy has to clear to be called new; Scalmalloy, the AlSi10Mg data sheets, Aheadd CP1 and **Taheri-Mousavi et al.'s alloy** in gray as context. Inset or SI: the front redrawn under the other burden metrics | **partial**: data-sheet values for all four alloys, checked Nov 27 (`data/scfree-baselines-datasheets.csv`, `data/benchmark-property-window.csv`); Utah AlSi10Mg; B_NIR for every baseline and seed (`tools/mineral_burden_check.py`). No baseline printed here yet; powders not bought (sourcing in #277's run) | B4, B5, B6 | campaign paper (first baseline prints), campaign 2 | Nov 2027 |
| d | The finalist: stress–strain curves (n ≥ 3), micrograph, outside composition and tensile | **none** | B5, V1, V2 | campaign 2 + outside labs | Dec 2027 |

## Fig. 6 When it pays off: the twin (§2.6)

| Panel | Content | Status | Needs | Supplied by | Due |
|---|---|---|---|---|---|
| a | Twin validation: simulated vs measured step time, cost, failure rate, usable-powder fraction, tensile scatter, AlSi10Mg yield | **partial, and off**: the round-2 audit (PR #293) found the twin at 6 % atomizer failures vs 8 of 10 failed in the lab, 5–8 runs/week vs 1.7, 91 % usable powder vs 52.4 %, 1–2 % yield scatter vs 5.7 %, 305 vs 228 MPa for AlSi10Mg; no simulator fitted to a lab measurement yet; desktop LPBF not modelled | T1 | twin (#276, byu-vcl PRs 393–394) refit on campaign 1 then campaign 2 records | Apr 2027, then Nov 2027 |
| b | Spend (and days) to a fixed target for the step-choosing policy (pKGFN or BOFN with powder reuse, decision M7) and its full-chain counterpart, screen-then-test, standard BO and random; ≥ 20 seeds; 95 % matched-seed bootstrap CIs; screen right (κ = 0) vs screen wrong (κ = 1) | **partial (synthetic)**: the BOFN paper set (issue #121; `benchmarks/bofn-paper/paper-stats/`, 20/16/16 matched seeds at κ = 1/0.5/0; in SI S14 and the draft panel below). κ = 1: 3.8× less spend than screen-then-test for BOFN with powder reuse (95 % CI 2.4–5.9) and for pKGFN (1.9–6.3); κ = 0: no network policy's mean reaches screen-then-test's $100k result (the M8 expectation), though its lead over the two BOFN policies isn't resolved. `bofn-clocked` (PR #297) agrees on time, not money: at κ = 0 screen-then-test reached T1 sooner than BOFN on 10 of 10 seeds, but BOFN was $18–39k cheaper. Both hand-built, not calibrated | T2 | twin after calibration | Dec 2027 |
| c | Advantage map: acceleration factor against screen error κ and the powder-to-calculation cost ratio, marking where the gain disappears | **partial (synthetic)**: the paper set gives the κ axis at three points (κ = 1, 0.5, 0: BOFN with powder reuse 3.8×, 1.2×, not reached; pKGFN 3.8×, not reached, not reached); the cost-ratio axis isn't run | T3 | calibrated twin | Dec 2027 |

## Tables

| # | Content | Status | Supplied by | Due |
|---|---|---|---|---|
| 1 | Each step's cost per result: median and IQR of person-hours, machine hours, consumables and $; **powder mass each node consumes and atomizer runs per tensile set**; n | none | L1–L2 | Nov 2027 |
| 2 | **Alloys against the baselines.** The finalist(s), then Al5X1, Al-HS1, AlSi10Mg (as built and stress-relieved) and Scalmalloy, each **in house** (same session) and **on its data sheet** in the matching condition and orientation. Columns: target and measured composition, density, hardness, YS/UTS/EL (n), B; the parity gap (in-house ÷ data sheet) for each baseline. Scalmalloy (data sheets) as context. Draft rows are in `manuscript.tex` | partial: data-sheet rows filled, with the April Utah AlSi10Mg | B4–B6, V1–V2 | Dec 2027 |

## Supporting Information (beyond S1–S9 above)

S17 the industry baselines: supplier, lot and certificate, ICP-OES of each lot against the supplier's composition, the parameters they were printed with (and any sweep), aging on the supplier's schedule and on the family curve, the parity table against the data sheets, and the front under each burden metric; S10 desktop LPBF design, commissioning, O₂ log and laser calibration; S11 every candidate in both campaigns with every measured output and why it stopped; S12 function-network model (nodes, kernels, costs, acquisition, batching, failure handling — #274, seeding — #275) and, from issue #121's short version, the model and the eight policies of the synthetic benchmark (**in**); S13 pre-registration of baselines, targets and stopping rule, dated before campaign 2, with decision M7 (the acquisition); S14 twin specification, calibration and per-seed results, plus the synthetic benchmark of the optimizer: why, workflow, protocol, results, validation, two figures and the 2 × 2 table (**in**; it shrinks to a summary and a citation if a MethodsX companion is published first); S15 SOPs (atomizer #251/#253, powder SEM prep, sieving, powder safety #267, desktop LPBF); S16 corrosion, if kept in (decision D6); S18 composition spread and fidelity (EDS settings and calibration, ICP-OES, Mg loss; Fig. 3). `supporting-information.tex` follows this numbering, and its build stops if S12, S13, S14 or S17 drift, because the manuscript cites them by number.

## Draft panels in this folder

| File | What | Source data |
|---|---|---|
| `figures/fig1-loop.tikz` | Schematic of the loop (draft for Fig. 1a) | none needed |
| `figures/figS-atomizer-runs.pdf` | Every atomizer run to date and how it ended (draft for SI S1/S3) | PR #286 `atomizer-runs/runs.csv` @ `8320f13` |
| `figures/fig5c-draft-benchmarks.pdf` | Yield strength against mineral burden: Al5X1 and Al-HS1 at their data-sheet values with the draft front they set above this lab's AlSi10Mg (the target region shaded); the Sc-free front on reported values as a dotted staircase (the bar for calling an alloy new); AlSi10Mg and Scalmalloy data sheets and Aheadd CP1 as context; the B ranges of the baselines and seeds (frame for Fig. 5c) | `data/scfree-baselines-datasheets.csv` (EOS and Höganäs documents, checked 2026-11-27), `data/benchmark-property-window.csv` (PR #285 @ `a25d763`), `data/literature-alloys-campaign-paper.csv` (#277 @ `baca180`), Utah AlSi10Mg n = 4 (PR #288), the campaign paper's MCS 2026 inputs via `tools/mineral_burden_check.py` |
| `figures/fig1a-draft-network-photos.pdf` | The loop with lab photographs (draft for Fig. 1a) | #284 @ `a68b67d` |
| `figures/fig6-draft-synthetic.pdf` | Best alloy printed and tested against new spend for seven of the eight policies (all but screen-then-test without powder reuse) at κ = 0, 0.5 and 1 (as in SI Fig. S2), with 95 % intervals and the spend ratio to screen-then-test's $100k result (draft layout for Fig. 6b) | `../benchmarks/bofn-paper/paper-stats/curves.csv` and `numbers.tex` (issue #121 at `18f5265`, copied unchanged; `make bofn-check`) |
