# Preliminary data

This folder collects the tensile and SEM/EDS results behind the "Preliminary results in hand"
line of [`grant-targeting-analysis.md`](../grant-targeting-analysis.md) (line 45), gathered for
[#282](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/282) on 2026-11-25.
Each folder has its own README with sources, method and caveats.

| Item on line 45 | What exists | Folder |
|---|---|---|
| AlSi10Mg tensile, University of Utah | **Yes.** Five room-temperature tests: raw MTS files, stress-strain plot, datasheet comparison | [`tensile-alsi10mg-utah/`](tensile-alsi10mg-utah/) |
| AlSi10Mg tensile, 3D Powder Tech | **Coupons, no tensile data.** Photos of as-printed coupons only | [`tensile-alsi10mg-3d-powder-tech/`](tensile-alsi10mg-3d-powder-tech/) |
| High-T tensile data | **None found** (below) | none |
| SEM/EDS of precursor (feedstock) powders | **Yes.** AlSi10Mg 40 µm, Si 100-200 mesh and Si 40 µm: EDAX mapping reports, SEM images | [`sem-eds-feedstock/`](sem-eds-feedstock/) |
| SEM/EDS of atomized powders | **Partly.** SEM of eight Al lots and one NAB lot from the lab's own atomizer (EDS: spectrum screenshots, plus one raw spectrum). **Nothing** for the AMAZEMET-atomized blend that the claim refers to | [`sem-eds-atomized-powders/`](sem-eds-atomized-powders/) |
| *Not on line 45:* standards-based EDS of AlSi10Mg | **Yes, on a printed part.** NIST DTSA-II against pure Al, Si and MgO standards, 17 runs on a polished Utah coupon. The one valid run gives Mg 0.35 and Si 11.1 wt % | [`eds-standards-alsi10mg-utah/`](eds-standards-alsi10mg-utah/) |

## Tensile results against the datasheets

All values are as built (no heat treatment) and at room temperature. Nikon's 95/95 minimum is in
brackets.

| Specimens | Yield Rp0.2 (MPa) | UTS (MPa) | Elongation after fracture (%) |
|---|---|---|---|
| **Utah, mean ± SD of tests 1, 2, 3, 5** (horizontal, near-net-shape) | **228 ± 13** | **376 ± 10** | **4.5 ± 0.5** |
| Utah, test 5 alone (the most reliable run) | 236 | 390 | 5.0 |
| 3D Powder Tech | no data | no data | no data |
| High temperature | no data | no data | no data |
| EOS M 290, 30 µm, horizontal, machined | 270 | 461 | 10.2 |
| EOS M 290, 30 µm, vertical, machined | 233 | 466 | 6.3 |
| Nikon SLM 280, 30 µm, horizontal, machined | 305 (300) | 465 (460) | 9 (6) |
| Nikon SLM 280, 30 µm, vertical, machined | 270 (255) | 475 (445) | 6 (3) |
| Nikon SLM 280, 30 µm, vertical, near-net-shape | 255 (240) | 425 (380) | 5 (2) |

- **How close we are.** The Utah coupons reach about 81 % of the datasheet UTS and 84 % of EOS's
  horizontal yield. Their elongation is half the machined horizontal values.
- **Closest datasheet row.** It is Nikon's near-net-shape row, the only one with as-printed
  surfaces. Test 5 sits just above its UTS minimum and just below its yield minimum.
- **Details.** Per-test values, the method and the caveats are in
  [`tensile-alsi10mg-utah/README.md`](tensile-alsi10mg-utah/README.md).

The datasheet sources are the EOS
[process data sheet for the EOS M 290, 30 µm](https://www.eos.info/metal-solutions/data-sheets/aluminium/pds-eos-aluminium-alsi10mg-eos-m-290-30um)
and Nikon SLM Solutions'
[MDS_AlSi10Mg_2025-11.1_EN](https://nikon-slm-solutions.com/wp-content/uploads/2025/11/mds5123.pdf)
(SLM 280 PRECISION), both read on 2026-11-25.

## Composition: standards-based EDS of a printed coupon

The CALIBER project ([vertical-cloud-lab/caliber](https://github.com/vertical-cloud-lab/caliber/issues/35))
quantified 17 EDS spectra of a polished Utah coupon in NIST DTSA-II. The standards were pure Al,
pure Si and MgO, measured on the same SEM and detector. Details are in
[`eds-standards-alsi10mg-utah/`](eds-standards-alsi10mg-utah/).

- **Valid result.** In the one valid run (5 kV, analytical total 1.03), Mg is 0.35 wt %, inside
  the 0.20-0.45 % specification. Si is 11.1 wt %, at the 11.0 % limit. Standardless EDS of the
  same alloy had given 1.4-1.6 wt % Mg.
- **The other 16 runs aren't usable yet.**
  - Most 10-25 kV runs used standards collected at 60-99 % dead time.
  - The 2026-11-18 runs were acquired at a different amp time from the standards (0.96 vs
    7.68 µs). That mismatch alone is enough to explain why their Mg reads about twice as high.
  - Two runs entered the MgO standard as pure Mg.
- **What it doesn't cover.** It is one run on one area of a printed part. There is no
  standards-based EDS of any powder yet.

## High-temperature tensile: none found

**No high-temperature tensile data exists anywhere on GitHub.**

- **What was searched:**
  - every branch of this repo, by file name and content;
  - every issue that mentions tensile;
  - byu-vcl's issues and its `main` branch.
- **Where the claim appears.** `grant-targeting-analysis.md` line 45 and several Edison
  documents list "high-T tensile data". `edison-trajectories/preliminary-results-roadmap.md`
  gives it as "standard aluminum specimen". All of them copy one list from PR #4's body, which
  came from the private repo.
- **What exists instead is plans:**
  - [byu-vcl#46](https://github.com/vertical-cloud-lab/byu-vcl/issues/46#issuecomment-4224586523)
    (2026-04-10) wants "some high-T testing on that tensile machine with the furnace";
  - [#138](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/138#issuecomment-6353372394)
    (2026-04-27) calls it a stretch goal;
  - the proposal on `consolidation-2` has an "Elevated-Temperature Tensile Tester [TBD
    specification---placeholder]";
  - [#256](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/256#issuecomment-7123300072)
    (2026-11-24) drops elevated-temperature tests from the campaign.
- **If a test was run,** the data would be on the lab's Box, on the MTS computer in BYU's
  testing lab, or in e-mail. It is not in this repo's imports of `digital-alloy-lab-private`
  (`main` and `consolidation-2`). The private repo itself was not checked.
- **Coupons for a test.** Five untested Utah coupons remain (see the Utah README).

## Elsewhere, not copied

- **Raw EDS spectra of the feedstock** are in
  [byu-vcl#48](https://github.com/vertical-cloud-lab/byu-vcl/issues/48#issuecomment-4274431356)
  (CSV/XML, 2026-04-18) and
  [byu-vcl#48](https://github.com/vertical-cloud-lab/byu-vcl/issues/48#issuecomment-4292370008)
  (`.msa`, 2026-04-21). byu-vcl is a different (public) repo, so they are linked rather than
  copied.
- **SEM/EDS of the printed Utah coupons** (fracture piece and polished section) is in
  [#138](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/138#issuecomment-6353376021).
  That is part data, not powder data.
- **The 3D Powder Tech spreadability report** is in #133. It isn't copied, for the reasons in
  [`tensile-alsi10mg-3d-powder-tech/`](tensile-alsi10mg-3d-powder-tech/).
