# Lower-expansion build plates, and when a 500 °C plate is worth building

Written 2026-11-19 for [PR #266](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/266) (issue #260), in answer to two
questions about [`modules.md`](modules.md):

1. "A 0.10 mm plate clearance seizes on Ø75 ... Is there a different material with a lower thermal expansion coefficient that would
   make sense to use?"
2. "The Tier B (500 °C) option needs a steel or ceramic heater block. Under what circumstances does this seem necessary to be able
   to go to 500 C? I.e., for what materials and for what kinds of applications. Though, I also wonder about other complications
   that come like powder spreadability and environment purity at these kinds of temperatures."

| File | What it is |
|---|---|
| [`analysis/out/thermal/plate_materials.md`](analysis/out/thermal/plate_materials.md) (+ `.json`) | CalculiX re-run of the build-start case with nine plate materials, at 200 °C (S25, M50, L75) and 500 °C (M50); properties and their sources |
| [`analysis/thermal_module.py`](analysis/thermal_module.py) `plates` | the mode that runs it; the existing modes and outputs are unchanged |
| [`plate-materials.csv`](plate-materials.csv) | plate stock for each candidate, read live from vendor pages through the lab Pi |
| [`preheat_500.py`](preheat_500.py) | each alloy's solidus against the set point, and the Mg, Zn, Li and Al vapour pressures at 200 and 500 °C |
| [`edison/preheat-500-plate-cte/`](edison/preheat-500-plate-cte/) | Edison `LITERATURE_HIGH` task on both questions: query, answer, references, full trajectory |

Nothing here has been built, quoted or reviewed by BYU's LSO or EHS.

## 1. A lower-expansion plate?

**Short answer.** For aluminium powders, only a little, and today's 6061 plates already work. The plate has to stay an Al alloy,
and the lowest-expansion Al alloys worth buying (4032, or a printed AlSi10Mg plate) cut the closing by ~20 %. For steel, Ni and Ti
powders, yes: their plates (410/430, 17-4 PH, 316L, Ti-6Al-4V) close 2–4 times less, so their diameters can be cut closer. At
500 °C the expansion matters much more, and the answer there is a hot-side seal over a wider gap, or an Al insert in a
low-expansion carrier ring (§1.3).

**Why the plate, not the bore.** The gap closes because the plate sits at ~200 °C while the 316L spigot around it stays at
52–59 °C at the start of a build (thermal FEA). The closing is R·(ᾱ_plate·ΔT_plate − ᾱ_bore·ΔT_bore), and ΔT_plate is about five
times ΔT_bore, so the plate's expansion sets the answer. Changing the bore barely helps: a 6061 spigot and tube carry the heat to
the floor so well that they run cooler (36–39 °C) and close the gap by the same amount, and the heater then needs 9–10 W more.

### 1.1 What the FEA gives (build start, the worst case)

`analysis/thermal_module.py plates` swaps only the plate: its conductivity in the FEA and its mean expansion from room temperature
to its own temperature in the clearance. The heater block stays 6061 and the bore 316L. Full tables and sources:
[`plate_materials.md`](analysis/out/thermal/plate_materials.md).

| Plate | Mean CTE to 200 °C (µm/m·K) | Closing at 200 °C, S25 / M50 / L75 (µm) | Least cold radial clearance for 25 µm hot (µm) | Plate centre − edge (°C) | For which powders |
|---|---|---|---|---|---|
| 6061-T6 (today) | 24.4 | 51 / 98 / 142 | 76 / 123 / 167 (today 100 / 150 / 200) | 1–2 | Al alloys |
| 4032-T6 (12 % Si piston alloy) | ≥ 19.4 | ≥ 39 / 75 / 108 | ≥ 64 / 100 / 133 | 1–2 | Al alloys |
| AlSi10Mg, printed, stress-relieved | ≥ 20.9 | ≥ 43 / 82 / 118 | ≥ 68 / 107 / 143 | 1–2 | AlSi10Mg |
| 316L | 16.1 | 32 / 59 / 85 | 57 / 84 / 110 | 10–11 | steels, Ni alloys |
| 17-4 PH, H1150 | 12.4 | 23 / 43 / 60 | 48 / 68 / 85 | 10–11 | steels, Ni alloys |
| 410 / 430 stainless | 10.6–10.7 | 19 / 35 / 48–49 | 44 / 60 / 73–74 | 7–8 | steels, Ni alloys |
| Ti-6Al-4V | 9.0 | 16 / 28 / 37 | 41 / 53 / 62 | 16–19 | Ti alloys |
| Invar 36 (a bound, not a candidate) | 3.1 | 2 / 1 / −3 | 27 / 26 / 22 | 15–17 | none |

"≥": the datasheet gives the CTE only to 100 °C, which under-states the closing (by ~5 µm on L75 if 4032's CTE rises like 6061's).

What this means:

1. **Today's per-size clearances work.** With 6061's mean CTE to 200 °C, the hot gap at build start is 49 / 52 / 58 µm
   (S25 / M50 / L75), a few µm under the figure in `thermal.md`, which used the 20–100 °C value. That still leaves more than 25 µm.
2. **For Al powders the plate must stay aluminium.** Al printed on steel, Ti or Cu forms brittle Fe-Al, Ti-Al or Cu-Al
   intermetallics and bonds poorly (Edison §3.2); Al-on-Al is the standard practice. 4032-T6 closes ≥ 108 µm on L75 against
   142 µm for 6061 (24 % less), so L75 could be cut to ≥ 0.13 mm instead of 0.17–0.20 mm. That doesn't get every module back to one
   0.10 mm clearance, and 4032 has not been qualified as an LPBF substrate in the literature Edison found (rank 9), so it would be
   a trial. The spray-formed hypereutectic Al-Si "controlled-expansion" alloys (Osprey CE17, CE13) would cut the closing further,
   but their datasheets are behind a login, so they were not run. Edison also cautions that hypereutectic Al-Si and Al-SiC are
   brittle, hard to machine and unqualified as substrates (rank 10).
3. **Plates for other powders close 2–4 times less, so size each for its own material.** The bore is fixed, so the plate
   diameter is what changes: on L75 a 430, 17-4 PH or Ti-6Al-4V plate needs only 0.07 / 0.085 / 0.06 mm cold. Cut to 6061's
   0.20 mm, they would run 140–163 µm hot, which lets powder and heat through.
4. **Low-conductivity plates cost temperature uniformity.** With the centre held at 200 °C, the edge runs 7–8 °C cooler on 430,
   10–11 °C on 17-4 PH and 316L, and 16–19 °C on Ti-6Al-4V (6061: 1–2 °C). The block also runs hotter: on S25 it reaches 228–241 °C
   against the 240 °C cutoff, so S25 with a steel or Ti plate needs a higher cutoff and block ceiling, or a thinner plate.

**Stock** for a Ø80 × 10 mm blank, read on McMaster-Carr through the lab Pi on 2026-11-19 ([`plate-materials.csv`](plate-materials.csv)):

| Plate | McMaster part | Price |
|---|---|---|
| 6061 | 1610T27, 3-1/4 in. rod cut 1/2 in. long | $9.97 |
| 316/316L | 9260K4, 3-1/2 × 1/2 in. disc | $46.58 |
| 17-4 PH | 1319T2, 3-1/2 × 1/2 in. disc, Condition A (age to H1150 yourself); 87205K61 is 4 in. rod already in H1150, $337.71 per 6 in. | $25.28 |
| 410 (the stocked stand-in for 430) | 86705K25, 3-1/4 in. rod | $155.95 per 6 in. |
| Ti-6Al-4V | 9257K14, 3-1/2 × 1/2 in. Grade 5 disc | $125.59 |
| 4032, AlSi10Mg, CE17, thick 430, Invar over 1 in. | not stocked: 4032 is quote-only from a mill, AlSi10Mg would be printed in-house | – |

### 1.2 What to do now

- Keep 6061 plates (or 5083 where they sit at 200 °C for long) with today's per-size clearances and the PTFE rim wiper.
- Make the plate diameter a per-material number in `module_params.py` when the first steel or Ti plates are made, from the
  table above, rather than one clearance per module.
- Try 4032 only if the L75 gap needs to be tighter; it is a test, not a drop-in swap.

### 1.3 At 500 °C (Tier B) the expansion becomes the main problem

- **Aluminium plates.** 6061 closes ≥ 281 µm on M50 at 500 °C (≥ 0.31 mm cold needed), and roughly 0.43 mm on L75 by hand
  (37.9 mm × (25.2·10⁻⁶ × 475 K − 16.0·10⁻⁶ × 40 K)). 500 °C is also 82 K under 6061's solidus and 30 K under 4032's, so neither is
  a structural part at that temperature. Edison's §3.1 and rank 6 put the radial closing at 0.18–0.21 mm, half of this: their
  0.36–0.41 mm "diametral" figure is the radial one.
- **Steel and Ti plates** (for steel and Ti powders) close 91–184 µm on M50 at 500 °C. Ti-6Al-4V is the cleanest: 430 sits in its
  475 °C embrittlement range, and 17-4 PH loses toughness above ~316 °C unless re-aged.
- **So for Al powders at 500 °C, take one of two routes:**
  - a ≥ 0.31 mm (M50) to ~0.45 mm (L75) cold gap closed by a compliant hot-side seal: graphite felt or foil, or a ceramic-fibre
    wiper, with a labyrinth and a powder-catch annulus. PTFE (~260 °C) and FKM (~200 °C) can't be used there. The piston is
    guided on its cool lower land, and the hot plate floats radially inside its gap (Edison ranks 7–8);
  - a sacrificial **aluminium insert in a low-expansion carrier ring** (Ti-6Al-4V or 17-4 PH). The carrier forms the sliding rim,
    the bayonet and the gripper groove; the insert sits in a pocket with its own gap and is the only part printed on (Edison
    rank 11). Not modelled yet.

## 2. When is a 500 °C plate worth building?

**Short answer.** For the Al screening this machine is for, rarely. 500 °C is the documented route to one result: crack-free
6xxx alloys (6061, 6182) **without changing their chemistry**. It doesn't fix 2xxx or 7xxx, and 500 °C is above 7075's solidus.
Grain refiners (Zr, Sc, Ti/TiB₂, CaB₆) get crack-free 6xxx and 7xxx at ≤ 200 °C, and AlSi10Mg and Al-Mg-Sc/Zr need no high
preheat at all. Outside aluminium, 500 °C pays for low-stress Ti-6Al-4V with its martensite decomposed in place, and for tool and
high-speed steels that still crack at 200 °C.
It is not enough for non-weldable Ni superalloys, TiAl, W or WC-Co, which need 800–1200 °C.

| Alloy class | What a hot plate did | 500 °C needed? | Without a hot plate |
|---|---|---|---|
| AlSi10Mg | prints crack-free from room temperature to 200 °C; heat mostly ages it in place (requirements-later.md §1) | no | – |
| Al-Mg-Sc/Zr (Scalmalloy) | crack-free cold; 200 °C is used for in-situ ageing, not crack control | no | Sc/Zr nucleate fine grains |
| 6xxx: 6061, 6082, 6182 | unmodified 6061 crack-free at 500 °C (Uddin et al., Addit. Manuf. 22 (2018) 405–415), but as-built YS ≈ 60 MPa, UTS ≈ 130 MPa (Edison: li2024); EN AW 6182, which already carries some Zr, equiaxed from 400 °C and crack-free at > 99 % density at 500 °C ([Riener et al. 2022](https://doi.org/10.1007/s00170-022-08673-8)) | **yes, if the chemistry stays unmodified** | Zr nanoparticles: crack-free 6061 and 7075 ([Martin et al. 2017](https://doi.org/10.1038/nature23894)); Zr + 100 °C, or TiAl₃ inoculation (Edison) |
| 7xxx: 7075 | 200 °C failed; 400 °C changed the cracks but didn't remove them, and ~1 wt % Zn and 0.3 wt % Mg evaporated (Velikajne 2026, requirements-later.md §1). **500 °C is above 7075's 477 °C solidus** | no: can't | Zr, Ti, Si + TiB₂ |
| 2xxx: 2024 | 200–400 °C reduced but did not remove cracking; 500 °C is at its 502 °C solidus | no: can't | Ti (1.5 wt %), CaB₆, Zr, Sc |
| H13 / 1.2344 hot-work steel | crack-free or close at ~200 °C in some windows; 400 °C gave a homogeneous bainitic structure ([Mertens et al. 2016](https://doi.org/10.1016/j.phpro.2016.08.092)); one powder still cracked at 500 °C | sometimes | scan strategy, chemistry |
| M2 high-speed steel | crack-free at 200 °C, 99.8 % dense ([Kempen et al. 2014](https://doi.org/10.1115/1.4028513)); other work saw cold cracks across 200–400 °C | sometimes | – |
| M50, HS6-5-8-3 and similar | improved progressively up to 500 °C; HS6-5-8-3 crack-free at 500 °C (Edison) | yes, for these | – |
| Ti-6Al-4V | crack-free cold; 570 °C cut residual stress sharply and decomposed α′ martensite to α + β in place, raising elongation by 66 % ([Ali et al. 2017](https://eprints.whiterose.ac.uk/114897)) | only for low-stress as-built parts | supports, scan strategy, stress relief afterwards |
| IN718 (weldable Ni) | crack-free cold; 80–500 °C changes stress and defects only | no | – |
| CM247LC, IN713LC, IN738LC, René 80 | still cracked at ~900 °C; > 1200 °C needed (Edison: abdelwahed2023) | 500 °C is not enough | alloy changes, HIP |
| γ-TiAl | ~800 °C ([Gussone et al. 2015](https://doi.org/10.1016/j.intermet.2015.07.005)) | not enough | – |
| W, WC-17Co | ~1000 °C and 900 °C (Edison) | not enough | – |

**Applications that would justify Tier B here:**
- a baseline for unmodified wrought 6xxx, to compare "hot plate" against "grain refiner" as two routes to crack-free parts;
- in-situ heat-treatment studies, where the plate temperature and time are recipe variables;
- Ti-6Al-4V or tool-steel coupons that must come off the plate stress-free, or thin walls that distort;
- later, M50 and high-speed steels.

**Where it is offered commercially:** TRUMPF's TruPrint 5000 has an optional 500 °C substrate preheat on its exchangeable
cylinder. TRUMPF cites H11 and H13 tool steels, ~95 % less cantilever deflection than at 200 °C, and a cool-down of up to 20 h
([TRUMPF](https://trumpf.com/en_GB/solutions/advantages-of-trumpf-machines/advantages-of-additive-production-systems/500c-preheating);
[Metal AM](https://www.metal-am.com/articles/reducing-residual-stress-with-500c-build-chamber-preheating-for-first-time-right-pbf-lb/)).
Others are an SLM 280 with a 500 °C system used for tool steels, the Aconity MIDI (500 °C standard, above 1000 °C custom; the
AconityMINI lists 800 °C as an option), and an EOS M 290-HT research machine with a 900 °C plate and VCSEL top heating to
1200 °C (Edison §1.6).

## 3. What changes at 500 °C: spreadability, purity, and the machine

### 3.1 How hot 500 °C is for an Al alloy

From [`preheat_500.py`](preheat_500.py) (solidus from ASM):

| Alloy | Solidus | 200 °C as a fraction of solidus (K/K) | 400 °C | 500 °C |
|---|---|---|---|---|
| 7075 | 477 °C | 0.63 | 0.90 | **1.03: above the solidus** |
| 2024 | 502 °C | 0.61 | 0.87 | **1.00** |
| AlSi10Mg | ~557 °C | 0.57 | 0.81 | 0.93 |
| 6061 | 582 °C | 0.55 | 0.79 | 0.90 |
| Ti-6Al-4V | ~1604 °C | 0.25 | 0.36 | 0.41 |

- **At 500 °C an Al powder bed is near its solidus.** It is close to 6061's 530 °C solution treatment, so the part is
  effectively solution-treated for the whole build and slow-cooled afterwards. That explains the soft as-built 6061 (YS ≈ 60 MPa);
  such parts need a full T6 (solution, quench, age) after the build. For Ti-6Al-4V, 500 °C is only 0.41 of the solidus, which is
  why a hot plate helps it without these side effects.
- **The plate is near its solidus too.** 6061 and 4032 plates and the 6061 heater block can't carry load at 500 °C (§1.3).

### 3.2 Spreadability

- **There is almost no Al data.** Edison found no controlled measurements of Al LPBF powder spreading at 400–600 °C. For Al, the
  literature points to moisture, oxide, condensate and fines as what controls cohesion.
- **Heat can help spreading at first.** A Ni powder (GH3536) went from non-flowing at 100–200 °C to its best spreading at 400 °C:
  its angle of repose fell from ~43° to ~27°, because the heat drove off moisture. Its oxygen rose to 478 ppm at 400 °C, though.
- **Over a long build, hot powder sinters.** Particles held hot form necks and agglomerates; the size distribution shifts
  coarse; agglomerates streak the layer, catch on the blade and leave lack-of-fusion defects. A review of Kempen's preheat work
  warns that too hot or too long a preheat sinters the loose powder. An Al bed at 0.9 of its solidus for hours is in the regime
  where the electron-beam machines run on purpose, and they need a powder-recovery step to break up the cake
  ([Kempen's preheat work, as reviewed in arXiv 1709.09510](https://arxiv.org/pdf/1709.09510)).
- **The recoater and dose path get hot.** They sit over and beside a 500 °C plate. Plan on an HSS or ceramic blade, blade-force
  monitoring, and powder with few fines (< 15 µm), and test hot spreading with the real powder before building (Edison
  rank 17).

### 3.3 Environment purity

- **Volatile elements leave much faster.** From 200 to 500 °C the equilibrium vapour pressure of pure Mg rises from 6 × 10⁻⁶ to
  10 Pa and that of Zn from 6 × 10⁻⁴ to 180 Pa: ×10⁵–10⁶ ([Alcock et al. 1984](https://doi.org/10.1179/cmq.1984.23.3.309)
  coefficients). For Zn in 7075 that is ~4 Pa as an ideal solution. At 200 °C the bed loses essentially nothing; at 500 °C the hot
  powder and the part lose Mg and Zn for the whole build, on top of the melt-pool losses. That shifts the composition being
  screened, and the vapour condenses on the window, the gas knife and the filter.
- **Oxygen does more damage.** Hot systems run below 200 ppm O₂ (EOS M 290-HT) or 100 ppm (Aconity). Edison recommends
  < 100 ppm before heating, and lower for Ti and Mg-rich Al. AlSi10Mg powder exposed to laser heat gained ~120 ppm O over five
  reuse cycles, against ~10 ppm for powder that saw no heat. Aluminium's own oxide stays amorphous and slow-growing until about
  550 °C, when it turns to γ-Al₂O₃ and oxidation speeds up
  ([Trunov et al. 2005](https://doi.org/10.1016/j.combustflame.2004.10.010)). So 500 °C is just under that step, but Mg in
  6xxx, 5xxx and AlSi10Mg oxidises sooner. Tungsten powder oxidised visibly at 600 °C even under flowing argon (Field 2020).
- **Water comes off the hardware.** A hot plate drives water out of the chamber walls, insulation, seals and the powder. Bake and
  purge the empty chamber before powder goes in, and measure dew point separately from O₂.
- **Powder from a hot build is its own lot.** Keep it apart from the general lot. Sieve it and test O, size distribution, flow
  and Mg/Zn before reusing it, and log each lot's time at temperature.

### 3.4 The machine (beyond what `modules.md` already reserves)

- The heater block becomes steel, a Ni alloy or a ceramic carrier, with Tier B's 120 V high-temperature cartridges
  (McMaster 3618K422). The piston head and flange are water-cooled, with the coolant flow interlocked to the heaters.
- The plate gets either a ≥ 0.31–0.45 mm gap with a graphite or ceramic-fibre seal, or the insert-in-carrier plate (§1.3).
- Shield or cool the window, cover-slide drawer, O₂ sampling line, recoater drive and hopper throat. Put the O₂ sensor in a
  cooled bypass. A 500 °C plate radiates about 7 times more than a 200 °C one (σT⁴: (773/473)⁴ ≈ 7).
- **Cool-down.** The lumped estimate is ~50 min for Ø50 to the 50 °C door interlock (requirements-later.md §1); TRUMPF quotes up
  to 20 h for its full-size cylinder. Parts also bond harder to a hot plate, so leave stock for sawing or EDM and for resurfacing
  the plate.

## 4. Recommendation

1. **Keep Tier B reserved, and screen crack-prone Al with grain refiners at ≤ 200 °C first.** Edison ranks this first and second.
   It also tests chemistry, which is what the lab screens, rather than the machine.
2. **Build Tier B only for a campaign that needs it:** an unmodified-6xxx baseline, Ti-6Al-4V or tool-steel coupons, or in-situ
   heat-treatment studies. Then:
   - build it on the S25 module first: it has the least heater power, the smallest gap change and the least powder at risk;
   - give that campaign its own powder lot and an O₂ limit < 100 ppm;
   - check the composition (Mg, Zn) of the built coupons against the powder.
3. **For Tier A, nothing changes.** Keep 6061 plates and today's clearances. When steel or Ti plates are added, size each from its
   own expansion (§1.1).
