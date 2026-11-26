# Data inventory: what the lab has collected so far (2026-11-26)

This counts the data the Vertical Cloud Lab has collected in 2026, across all of its public GitHub
repos, with alloy discovery and qualification first. It corrects the count posted on
[PR #288](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/288) on 2026-11-26. That
count covered only this repo, so it missed the AirGradient history after Oct 3, MongoDB, most
camera photos, the robot-arm tests and every other project. The one-slide summary is
[`infographic/`](infographic/).

**How it was counted.** Every branch of each repo was listed with the git trees API, and each
file was counted once even when it sits on several branches. Those file counts are exact. Labels
such as "camera still" or "render" come from file and folder names, so they are approximate.
Issue and PR counts come from the GitHub API (issue comments only, not review comments). "~"
marks an estimate. Files copied between repos (for example the atomizer training material, which
is in both byu-vcl and this repo) are counted in each.

## Totals (the infographic's top row)

| | Count | Basis |
|---|---|---|
| Files | **~41,000** | 41,398 in six repos: byu-vcl 11,797, digital-alloy-lab 10,291, powder-doser 9,549, tensegrity-optimization 7,115, robot-arms 1,955, digital-wetlab 691. caliber, custom-induction-furnace and streamingLambda are small and not totalled |
| Images | **~12,000** | 10,410 committed in five repos (byu-vcl 3,879, powder-doser 2,486, digital-alloy-lab 1,990, tensegrity-optimization 1,349, robot-arms 706), plus about 2,000 attached to issues and PRs |
| Camera stills among them | **at least ~1,700** | about 1,300 identified in byu-vcl and powder-doser (OT-2 cameras 536, CubXL cameras 262, 3D-printer cameras 331, powder-doser rig 84, atomizer and lab photos 82), about 230 in robot-arms, and about 350 photos and frames in this repo, besides its 433 video keyframes. The rest are SEM images, plots, renders and screenshots |
| Video | **~2,700 h** | 355 archived livestreams of the OT-2 and powder-doser cameras, about 2,640 h (Jul 30 - Sep 25, from streamingLambda's uptime study); 74 atomizer and training videos, 35 h; 24 robot-arm and 34 tensegrity YouTube videos. The repos also hold 771 video files, most of them renders |
| Sensor and balance readings | **~500,000** | AirGradient 327,349 raw readings to Oct 28 (exact); powder-doser balance about 150,000-250,000 (estimated from 15 MB of CSV); MongoDB colour sensor about 1,000-2,000 |
| Physical tests and runs | **~4,300** | tensegrity drop tests about 3,663 (to Aug 19); powder dosing and flow 392; CubXL runs 76; robot-arm runs about 30 and 11 camera calibrations; colour-sensor sessions 23; EDS 35 spectra; potentiostat 13; atomizer 10; tensile 5 |
| Issues and PRs | **1,267, with 10,655 comments** | byu-vcl 339 / 3,824; digital-alloy-lab 296 / 1,229; powder-doser 215 / 2,301; tensegrity-optimization 142 / 1,649; digital-wetlab 97 / 237; robot-arms 86 / 530; caliber 37 / 444; streamingLambda 20 / 89; custom-induction-furnace 19 / 323; structural-alloy-sdl-workshop 16 / 29 |

## What the first count missed

| Item | Corrected count | Where |
|---|---|---|
| **AirGradient** (one AirGradient ONE in CB 154, installed Feb 5, moved into the powder enclosure Sep 29) | **62,189** five-minute records from Feb 5 to Oct 28 (exact; 82 % of possible slots, gaps in Aug-Sep), averaging **327,349** raw readings of about 15 values each. The earlier 55,400 + 6,700 stopped at Oct 3. About 8,300 more five-minute records, through Nov 26, are only in AirGradient's cloud | byu-vcl branches, the issue-305 branch for Sep 29 - Oct 28; [#188](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/188), [#192](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/192) here |
| **MongoDB** (database `digital-wetlab`, documented in byu-vcl's `CLAUDE.md`) | `sensor-data`, the wireless colour sensor on the OT-2: about 1,000-2,000 documents, estimated from 1,825 readings committed in 42 JSON files across 22 sessions (Jul 27 - Nov 17). `ot2-runs`: no count anywhere. `powder_doser.battery_runs` (a separate cluster): 26 documents as of Sep 4. AirGradient does not write to MongoDB | byu-vcl, powder-doser issue 148 |
| **Camera photos** | at least ~1,700 camera stills, among ~12,000 images (above) | byu-vcl, powder-doser, robot-arms, this repo |
| **Robot arms** (AgileX PiPER) | about 30 logged runs on the real arm (tape pick-and-place stages 1-3, power and E-stop tests; 18 motion traces, 21 logs, Oct 9 - Nov 6); 11 camera-calibration sessions; 15 agent-written policy episodes, simulated (Nov 25-26); 11 simulated powder-doser workflow tests; 7 print jobs with 118 photos | robot-arms |
| **Livestreams** | 355 archived recordings, about 2,640 h, 96.8 % uptime (Jul 30 - Sep 25); 531 broadcasts catalogued across 10 cameras | streamingLambda |
| **Powder doser** | 139 doses in 30 runs over 13 powders, AlSi10Mg among them (99 pass QC, Aug 4 - Sep 15); 120 optimization trials, 10 of them dosing Al 4047 into atomizer cups (Sep 29 - Oct 21); 133 stepped-tilt flow trials, 26 of them AlSi10Mg (Nov 18-20); 128 rig-check captures; about 600 simulation files | powder-doser |
| **CubXL** | 76 run folders (pipetting tests and stirrer trials) with stills from two Pi cameras | byu-vcl `cubos/` |
| **Tensegrity** | about 3,663 drop-tower tests on about 50 printed specimens (May 22 - Aug 19; later drops not counted); about 1,830 simulation and BO output files | tensegrity-optimization |
| **CALIBER** | the 32 coupon and standard spectra already in [`eds-standards-alsi10mg-utah/`](eds-standards-alsi10mg-utah/); bronze powder EDS at 10, 15 and 20 kV with 12 Monte Carlo spectra (Oct 28); EBSD example data | caliber |

The induction furnace's data (50 runs, SEM, EBSD and optical micrographs) is from 2019-2020 and
was moved into `custom-induction-furnace` in June 2026 for the manuscript, so it isn't in the
2026 totals. `digital-wetlab` holds plans, a PHREEQC simulation and 98 rendered animations, but
little measured data. `structural-alloy-sdl-workshop` holds planning documents only.

## Alloy discovery and qualification (this repo)

These counts are unchanged from the first count.

| Stage | Data | Where |
|---|---|---|
| Design | about 1,250 simulated BO campaigns: 460 BOFN Al/LPBF runs (#122), 257 Cu/DED runs (#206, #224), 440 HPC array jobs (#14, #66), 60 LLM warm-start runs (`main`); 8,256 Eagar-Tsai evaluations (#238, #249); a 555-composition pycalphad grid; 18 DEM, 21 CFD and 20 FEA runs; no in-house Thermo-Calc calculations | branches named |
| Literature | 290 logged Edison tasks, about 500 reports in all; 841 BibTeX entries | `edison-trajectories/`, PR branches |
| Make | 10 atomizer runs (5 Al, 5 630 bronze), 13 lot codes; 984.6 g of bronze below 250 µm weighed on Oct 27, about 0.6 kg estimated on Nov 10 | [#286](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/286) |
| Characterize | 5,937 particles sized from 9 SEM fields of lot k7m2q9 ([#226](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/226)); about 45 SEM images of feedstock and atomized lots | [`sem-eds-atomized-powders/`](sem-eds-atomized-powders/), [`sem-eds-feedstock/`](sem-eds-feedstock/) |
| Composition | 17 runs and 15 standards on a polished Utah coupon, 1 run valid: Mg 0.35, Si 11.1 wt % | [`eds-standards-alsi10mg-utah/`](eds-standards-alsi10mg-utah/) |
| Qualify | 5 tensile tests of 10 AlSi10Mg coupons printed at Utah; no high-temperature tests | [`tensile-alsi10mg-utah/`](tensile-alsi10mg-utah/) |
| Corrosion | 13 potentiostat runs on dummy loads to check the instrument; no alloy yet | [#239](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/239) |
| Records | 74 atomizer run and training videos (35 h), transcripts of about 40 recordings, 4 SOPs | [#173](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/173), [#178](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/178), YouTube |

## Not counted

- **Photos stored on the atomizer camera Pis.** All three were offline on the tailnet on
  2026-11-26 (two last seen Nov 9, one Nov 17), so their disks couldn't be checked.
- **MongoDB itself.** This repo's Actions have no MongoDB credentials, so its counts are
  estimates from committed copies.
- AirGradient data after Oct 28, livestreams after Sep 25, tensegrity drops after Aug 19, the
  private Hugging Face Spaces, Box, Slack and deleted branches.
- Whether issue images are photos or screenshots: GitHub rate-limited the check.
