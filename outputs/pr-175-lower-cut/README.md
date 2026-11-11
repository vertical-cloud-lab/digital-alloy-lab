# The lower cut for the Al LPBF powder, and a shaker for the 8 in stack (PR #175)

The evidence behind the 2026-10-28 recommendation in
[`docs/sieve-order.md`](../../docs/sieve-order.md#the-lower-cut-revisited-2026-10-28). It covers three questions:
does our Al powder have enough below 15–20 µm to matter, how a lab could cut it out, and whether the 8 in stack
needs a shaker. Prices were read on 2026-10-28. McMaster and Gilson were read in the panel Pi's Chromium, the
rest from the web, and prices marked *(unverified)* come from a search index or a page that blocked the runner. No
order was placed, drafted or quoted.

## 1. How much of our powder is below 20 µm

No image PSD of an Al lot exists yet: #159 has only the first SEM look ("around 40–60 µm for the smaller
particles"). The one quantitative PSD from our atomizer is the NAB lot `k7m2q9` from PR #226 (5,937 particles,
SEM, edge-corrected). Its fine end, recomputed here and independently by the Edison analysis below, which agree:

| | Below 20 µm, by number | Below 20 µm, by mass | Below 15 µm, by mass |
|---|---:|---:|---:|
| Whole lot | 2.1 % | 0.016 % | 0.007 % |
| Of what passes 63 µm | 2.4 % | **0.05 %** (0.04–0.09) | 0.02 % |
| Of what passes 45 µm | 4.9 % | **0.19 %** (0.12–0.31) | 0.08 % |
| Al-12Si estimate, of what passes 45 µm | — | 0.63 % (0.35–1.14) | 0.29 % |

Intervals are 95 % field-bootstrap intervals, which allow for the size segregation on the stub. Particles under
10 px (about 7–10 µm) were not counted, and the Edison analysis showed that neither a log-normal nor a
Rosin–Rammler fit bounds how many were missed. By mass, though, a hidden population would have to be large to
matter.

**Al from the same atomizer should be coarser, not finer.** Lang's ultrasonic-atomization scaling,
d = 0.34 (8πσ/ρf²)^(1/3), at the same frequency gives Al-12Si droplets 1.26× the NAB size (1.22–1.30 over the
liquid-property ranges). That is consistent with the SEM note. The NAB distribution rescaled by 1.26 is the "Al-12Si
estimate" row above. It puts the number median near 59 µm, below 20 µm at 1.6 % by number and 0.007 % by mass, and
it also says something about yield:

| Of 100 g of powder | NAB, measured | Al-12Si, rescaled estimate |
|---|---:|---:|
| Passes 63 µm | 30 g (14–54) | **17 g** (8–30) |
| Passes 45 µm | 9 g (4–16) | **1.2 g** (0.5–2.2) |

So the top cut, not the bottom, decides how much print powder a run gives. This is one stub of a different alloy
transferred by a median scaling law, so treat it as a warning, not a number. Yankin et al. 2025 passed about 75 % of
their ultrasonically atomized AlSi12 through 63 µm. Our NAB lot had a coarse tail (13.5 % of its volume above
200 µm), which may come from our melt delivery rather than the alloy.

For scale, commercial gas-atomized AlSi10Mg that prints well has a volume D10 of about 18–27 µm (Weiss et al. 2022;
Warner et al. 2026, via Edison), i.e. about 10 % of its mass is below 18–27 µm. That is tens to hundreds of times more fines
than the numbers above.

## 2. What the literature says (Edison Q1)

- **Ultrasonic-atomization papers mostly cut only the top.** Yankin et al. 2025 (AlSi12, 63 µm only), Bashmakova et
  al. 2026 (316L, 53 µm only) and Ge et al. 2025 (preprint; Al-Zr-Er-Ni on a rePOWDER, Q10 = 33.6 µm, no cut
  reported, > 99.95 % dense prints). Two cut both ends with a sieve shaker: Grzelak et al. 2022 (316L, 20–63 µm, 92 % already
  in range) and Bałasz et al. 2023 (Ti64, 63 ± 20 µm).
- **Specs:** SLM Solutions 20–63 µm, EOS 25–70 µm. Open specs rarely give a maximum percentage below 15 or 20 µm; the
  D10 does that job.
- **Fines and Al:** cohesion grows as 1/(ρd²), so Al fines are more cohesive than steel fines of the same size.
  - Loss of fines on reuse improves Al powder flow (Weiss 2022, Warner 2026).
  - The finest sieved AlSi10Mg fraction packs worst in thin layers but absorbs best (Solyaev et al. 2026).
  - Where fines matter most: thin layers (≤ 30 µm), humid storage, blade or rubber recoaters.
- **Verdict:** no lower cut is defensible for single tracks, cubes and test bars, provided the paper reports:
  - the PSD by laser diffraction or calibrated image analysis;
  - one flow measurement (Hall or Carney, or avalanche angle);
  - apparent and tap density;
  - oxygen.

  Revisit if laser diffraction shows more than a few per cent by volume below 20 µm, or the powder flows as a
  cohesive one.
- **Safety does not change.** Removing fines raises the minimum ignition energy: about 6 mJ for 8–20 µm Al, 14 mJ
  for 20–37 µm and 48 mJ above 37 µm (as cited by Wu et al. 2010). Even 40 µm Al stays explosible (MEC about 35 g/m³), so every
  NFPA 484 precaution still applies.

## 3. Ways to make a 15–25 µm lower cut (Edison Q2, vendor pages)

| Option | Cost | 200–500 g lot | Blinding, losses | Al dust | Verdict |
|---|---|---|---|---|---|
| 8 in No. 635 (20 µm) with backing cloth, on a shaker | Gilson [V8SF #635 BU](https://www.globalgilson.com/8-sieve-all-stainless-full-height-635-with-back-up-cloth) $545.00 (without cloth $522.80); No. 500 (25 µm) $233.80. McMaster stops at No. 325. | DIN 66165 allows ≤ 7 cm³ (about 10 g) retained on a 25 µm, 200 mm sieve. Nearly all our powder is retained, so about 10 g a pass, i.e. 20–50 passes | Severe: dry sieving is "deficient" below about 45 µm (Neikov & Yefimov 2019); near-mesh wedging, static, mesh stretch | Open transfers and brushing | **No** |
| 8 in No. 450 (32 µm) with backing cloth | [V8SF #450 BU](https://www.globalgilson.com/8-sieve-all-stainless-full-height-450-with-back-up-cloth) $231.60 (without $209.50) | About 10–12 g retained a pass | High; a broad 20–45 µm transition | Same | Marginal. It also throws away real powder at 32–45 µm |
| Wet sieving | Low | Slow, then hours of drying | Drying re-agglomerates the powder | Water evolves H₂ and oxidizes Al; alcohols add a flammable solvent | **No.** No case of wet-sieved Al printed by LPBF was found |
| Sonic sifter | Gilson [GilSonic UltraSiever GA-8](https://www.globalgilson.com/gilsonic-8-inch-ultrasiever) $9,109.40 (8 in, up to 100 g, "10 g or less" below 20 µm); ATM/Advantech L3P $8,894 new (Gardco), $2,000 used *(unverified)* | Up to 100 g a run, about 10 g at fine cuts | Medium | Repeated loading | Measuring tool, not a production cut |
| Air-jet sieve | Gilson [Mikro Air Jet Sieve AJ-103B](https://www.globalgilson.com/mikro-air-jet-sieve) (8 in) $7,788.80; Retsch AS 200 jet $13.5–15.2k new *(unverified)*, $5,500 refurbished ([ALT](https://americanlaboratorytrading.com/lab-equipment-products/retsch-as-200-jet-air-jet-sieving-machine-22668/)); NEXOPART (Alpine) e200 LS $12.5–29.9k plus a $2,268 vacuum ([W.S. Tyler](https://blog-oh.haverboecker.com/alpine/alpine-air-jet-sieve-purchase)) | 0.3–100 g a run ([Retsch](https://www.retsch.com/products/sieving/sieve-shakers/as-200-jet/)). The > 20 µm product stays on the sieve, so it is a real lower cut, a few to tens of runs a lot | Low; the nozzle clears the mesh | The fines go into a vacuum cleaner, which must be rated for Al dust, with a cyclone | Best in-house cut, but analytical-scale and needs a dust-rated vacuum |
| Benchtop air classifier (Alpine 50 ATP, NETZSCH CFS 5 HD-S, Matsubo Elbow-Jet) | No public prices; Edison puts it above €50k | Fast once running | Hold-up in feeder, cyclone and filter is a large share of a 200 g lot | Needs closed inert-gas loop and explosion protection | Technically best (Cui et al. 2023 removed < 20 µm from a duplex steel with an Alpine 50 ATP before a 63 µm sieve), but not for this lab |
| Toll classification | Per lot | No published minimums; 200–500 g is likely below them | Edison expects large relative losses on small lots | Off campus; shipping Al powder | Worth asking once kilograms accumulate: [Elcan](https://elcanindustries.com/case_studies/aluminum-powder-screening) documents screening Al AM powder at 74 and 25 µm under N₂; Valimet lists custom size distributions (an option through the partnership) |

**On campus:** no sonic sifter, air-jet sieve or air classifier was found at BYU. Chemistry lists unnamed "particle
size analyzers" ([page](https://chem.byu.edu/department/research-facilities-and-instruments/)).

**To measure the fines,** two options:
- **BYU Electron Microscopy Facility:** SEM time is $30/h for Engineering users ([services](https://microscopy.byu.edu/services)), enough to count fines at higher magnification.
- **University of Utah Particle Size & Characterization Lab:** Sympatec HELOS/KF laser diffraction for outside users at $9.10 per dry sample plus $64.40 cleaning per job ([pricing](https://earth.utah.edu/research_facilities/earth-core-facility/pssc/pricing.php)). Its pages don't say whether it accepts combustible metal powder. Utah's MSE characterization lab also has a Beckman Coulter LS230 ([equipment](https://mcl.mse.utah.edu/equipment/)).

## 4. A shaker for the 8 in stack

The charge per pass, from DIN 66165 as [tabulated by Retsch](https://www.retsch.com/files/8698/info-test-sieve-charge.pdf)
for 200 mm sieves:

| Sieve | Max. batch | Max. retained | Retained mass at 1.3–1.5 g/cm³ |
|---|---:|---:|---:|
| 63 µm | 26 cm³ | 13 cm³ | 17–20 g |
| 45 µm | 20 cm³ | 10 cm³ | 13–15 g |
| 25 µm | 14 cm³ | 7 cm³ | 9–11 g |

Most of an Al run is retained on the No. 230, so a pass takes about 20–25 g, and a 100–250 g run takes 5–12 passes.
One layer of 50 µm Al on an 8 in mesh (about 300 cm²) is about 2.4 g.

- **63 µm by hand:** adequate for now, with the cover on and about 20–25 g a pass. Most particles are well away from
  the aperture.
- **45 µm by hand:** not adequate as a routine method. The cut sits near the number median (about 47 µm for the NAB,
  about 59 µm estimated for Al), where completeness depends on agitation and time. ASTM B214 and ISO 4497 specify a
  mechanical shaker with rotary and tapping action, and Edison Q2 calls a shaker essential at 45 µm.

| Shaker | New | Used / refurbished | Notes |
|---|---:|---:|---|
| W.S. Tyler Ro-Tap RX-29 (rotary + tapping, the ASTM B214 motion) | $3,459.56 ([Solutions Direct](https://solutionsdirectonline.com/ws-tyler-rx-29-ro-tap-sieve-shaker-for-8inch-test-sieves)); $3,762.40 ([Gilson SS-30](https://www.globalgilson.com/ws-tyler-ro-tap-sieve-shakers)); $4,206 (Gardco) | $1,850 ([HGR24 via Surplus Record](https://surplusrecord.com/listing/8-ro-tap-rx-29-ro-tap-sieve-shaker-0-25-hp-115-230-v-745914/)), $2,950 with sound enclosure; $1,950–2,250 dealer-tested (sold out); recent sales $1,499–1,500 | **Recommended**, used. Loud; an enclosure helps |
| Gilson SS-8R tapping | $3,824.60 ([Gilson](https://www.globalgilson.com/gilson-tapping-sieve-shakers)) | $1,550 with enclosure ([American Instrument Exchange](https://www.americaninstrument.com/products/gilson-sieve-shaker-with-sound-enclosure-4878e-sieve)) | Rated 1 in to No. 635 |
| Gilson SS-10 8 in vibratory | $4,180.70 ([Gilson](https://www.globalgilson.com/gilson-8in-vibratory-sieve-shaker)) | | No. 10 to No. 635, 8 full-height sieves, programmable |
| McMaster 3323K12 | $1,420.73 ([McMaster](https://www.mcmaster.com/3323K12/)), "Delivers Friday via freight" | | Cheapest new: 10 of our 8 × 2 in sieves, vertical + horizontal vibration, 30 min timer. Built for aggregate testing (ASTM C136), unproven at 45 µm. 45 in tall |
| Gilson SS-15 orbital | $1,867.20 | | Gilson rates it only down to No. 200 (75 µm): **not for 45 µm** |
| Gilson SS-23 wet/dry vibrator | $591.00 ([Gilson](https://www.globalgilson.com/wetdry-sieve-vibrator)) | | One or two 8 in sieves; a cheap aid for scalping, not a stack shaker |

Any shaker motor is an ignition source. Run it with the stack covered and bonded, in the hood, and let the dust
settle before opening, as in the doc's safety section.

## Files

- [`edison/`](edison/): queries and runner ([`run_edison.py`](edison/run_edison.py)), task IDs, answers, metadata,
  scrubbed trajectories and every file the tasks wrote:
  - [Q1](edison/q1_fines_in_lpbf_al.md): `LITERATURE_HIGH`, does the sub-20 µm fraction matter for LPBF of Al.
  - [Q2](edison/q2_lower_cut_methods.md): `LITERATURE_HIGH`, lab methods for a lower cut, and hand sieving against
    a shaker; plus its comparison table.
  - [Q3](edison/q3_psd_analysis.md): `ANALYSIS` of the PR #226 particle table. The notebook, code, CSVs and figures
    are in [`q3_psd_analysis_files/outputs/`](edison/q3_psd_analysis_files/outputs/), for example
    [`cumulative_fine_zoom.png`](edison/q3_psd_analysis_files/outputs/cumulative_fine_zoom.png).
- **Not committed:** the two literature tasks' pickled PaperQA document stores (70 and 127 MB, over GitHub's file
  limit) and the analysis's zip bundle (a copy of `outputs/` plus our own inputs). Their IDs are in the
  `*_files.json` listings.

![Cumulative number and volume fractions, NAB and the Al-12Si estimate, with 15, 20, 45 and 63 µm marked](edison/q3_psd_analysis_files/outputs/cumulative_fine_zoom.png)
