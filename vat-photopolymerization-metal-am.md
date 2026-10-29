# Vat-Photopolymerization Metal AM: Greene Group's PureForm

Issue [#228](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/228). Researched on 2026-10-29 from
public web sources only; nothing here comes from talking to Greene Group.

## Bottom line

- **What it is.** Greene Group Industries (GGI), a metal injection molding (MIM) contract manufacturer for medical
  devices in Oceanside, CA, sells metal parts made with **PureForm™**. A DLP printer cures a slurry of MIM powder in a
  photopolymer binder one layer at a time. The green parts are then debound and sintered on a MIM line. GGI got the
  technology when it bought Holo's assets in March 2024.
- **What it offers today.** It is a parts service, and GGI does not sell the printer. The only materials are
  **17-4PH and 316 stainless**. Parts come out with MIM-like fine detail without a mold: 0.07 mm walls, 0.2 mm holes,
  ±0.025 mm up to 12 mm, and 0.8–1.6 µm Ra as printed. Parts top out at about softball size, and walls at 3.5 mm thick.
- **Fit for FLAIME's aluminum alloys: none.** No vendor of this kind of process offers aluminum. The only published
  work found is academic DLP of AlSi10Mg, sintered at 600 °C in nitrogen (2021, see the Edison section below), with
  no final density or strength that Edison could check. The usual way to make aluminum sinter is a Mg addition, and
  Mg is one of the minerals FLAIME's alloys are designed to avoid. Even if the process worked, hours at sintering
  temperature would undo the rapid-solidification supersaturation that the Al-Zr and Al-Mn-Cr-Zr designs depend on.
- **Fit for the Cu-Cr-Zr complement: unproven and harder than it looks; one conversation in Phase II at most.**
  PureForm started as a pure-copper process (>92% IACS, a Holo-reported figure that nobody has checked
  independently). GGI's MIM line already sinters copper, and MIM-grade C18150 powder is on the market. Nobody has
  published Cu-Cr-Zr made this way, though. The closest work, a 2026 TU Wien thesis on GRCop-42 (Cu-Cr-Nb) by LMM,
  found that pressureless sintering didn't densify it without a liquid-phase additive. GGI doesn't list copper for
  PureForm today.
- **Who funds it (US government): very little, and no program targets it.** Section "Who funds it" below has the
  award search. The one squarely on-topic federal grant is an NSF CMMI Advanced Manufacturing CAREER award to Michigan
  State (2023–28, $567k). The others are a 2015–18 NASA SBIR and three 1996–98 DoD SBIRs, plus basic-science and
  space-technology grants (DOE BES, NASA, ONR, ARO, NIH, DoD) behind the photopolymer-template and salt-infusion routes
  such as Caltech's hydrogel infusion. ARPA-E has funded none of it. Holo, GGI, Incus, Admatec, Tethon 3D and Trio
  Labs have no SBIR/STTR awards; the companies are privately or EU funded.
- **Formulation work on the lab's OT-2: best for hydrogel infusion, not FLAIME's alloys.** Hydrogel infusion sets the
  alloy with an aqueous metal-salt bath at 70 °C, which the digital-wetlab OT-2 is set up to mix. I found no published
  map from bath composition to alloy composition. Hydrogen reduces only metals such as Cu, Ni, Co and Fe, though, so
  Al, Zr and Cr are out. For powder slurries the OT-2 can mix binders and screen viscosity, but cure depth and
  debinding carbon are measured off the deck. Section "Formulation work on the OT-2" below has the details.

## What PureForm is

ISO/ASTM 52900 puts this process under vat photopolymerization (VPP), but PureForm has no vat. It is a bottom-up DLP
printer. Each layer, a fresh film of slurry on a carrier film slides under the window, and the parts, hanging from
the build plate, dip into it. A projector cures the layer through the window. After printing, parts are cleaned,
debound and sintered "to their pure metal, final dimensions". There is no vat or powder bed to hold parts up, so
overhangs over 0.125 mm and bridges over 0.50 mm need supports. Ramps steeper than 30° support themselves. GGI says
the back end is "virtually identical to MIM" and uses MIM-type powders, so a part can move to molded production as
volumes grow without changing powder, furnace or supplier.

Numbers from GGI's [PureForm design guide (R3)](https://www.greenegroup.com/wp-content/uploads/2026/04/600-00001_Pureform_Design_Guide_R3.pdf):

| Spec | Value |
|---|---|
| Printer | GGI "H200", bottom-up DLP, load cell on the build plate |
| Materials (PureForm) | 17-4PH and 316 stainless ([product page](https://www.greenegroup.com/capabilities/metal-3d-printing/)) |
| Part size | "from a softball to a grain of rice"; no build volume published |
| As-printed surface finish | 0.8–1.6 µm Ra (smoother with post-processing) |
| Tolerance | ±0.025 mm up to 12 mm; ±0.2% above |
| Wall thickness | 0.07 mm min, 3.5 mm max |
| Gap between walls | 0.10 mm min at 12:1 aspect ratio |
| Holes and posts | 0.20 mm min diameter, 20:1 max aspect ratio |
| Fillet; base-layer feature | 0.05 mm min; 0.125 mm min in the shortest direction |
| Sintered parts | "comply with MPIF-35 standards"; "MIM-like microstructures and material properties" |

GGI publishes no density, tensile, lead-time or price figures for PureForm parts. For reference, GGI's
[MIM materials list](https://www.greenegroup.com/wp-content/uploads/2026/02/MIMMaterialsList.pdf) (Rev A, June 2024)
gives minimums of 7.6 g/cm³ and 970 MPa yield for MIM 17-4PH (H900), and 7.8 g/cm³ and 150 MPa yield for MIM 316L.
The same list covers 4140, 4340, 420A, 465PH, Ti-6Al-4V, a W-Ni-Fe heavy alloy, pure Cu (≥8.7 g/cm³), alumina and
zirconia. It has no aluminum.

The company is ISO 9001 and ISO 13485 certified, and Tinicum (private equity) has held a controlling interest since
2023. It has three sites: Oceanside, CA (headquarters and manufacturing), Port Huron, MI (MIM) and Newark, CA (Holo's
old home, now GGI's metal 3D printing development center). GGI pitches PureForm for prototypes and low-volume
production, mostly of medical parts ("weeks, not months";
[GGI, March 2026](https://www.greenegroup.com/pureform-prototype-to-production/)).

## Where it came from: Holo, 2017–2024

- Holo, Inc. was founded in 2017 in Newark, CA as an Autodesk spin-out. One co-founder had earlier built the DLP
  printer start-up that became Autodesk's Ember. Investors included Lightspeed, Prelude Ventures and Lam Research
  (Series B, 2021), plus Intuitive Surgical and Autodesk
  ([Global Venturing, 2023](https://globalventuring.com/corporate/industrial/holo-3d-metals-printing/)).
- PureForm launched in March 2021 with 99.9% pure copper, aimed at computing and EV cooling, RF and electrical
  interconnects. Holo sold parts, not printers, and was already sampling stainless steel
  ([DEVELOP3D, 2021](https://develop3d.com/3d-printing/holo-pureform-launched-for-copper-3d-printing/)). In January
  2021 Holo reported 25 µm layers and copper densities of 96–98% on average. It said it designs its binders in-house,
  buys powder from partners, and planned to add aluminum and ceramics. Aluminum never appeared in its offering
  ([Additive Manufacturing, 2021](https://www.additivemanufacturing.media/articles/the-case-for-tackling-the-toughest-material-first)).
- Holo and 5N Plus reported DLP-printed high-purity copper above 92% IACS with 100 µm features. CFD showed a printed
  cold plate cooling about 4 °C better than a conventionally made one
  ([ASTM STP1637, 2022, doi:10.1520/STP163720200122](https://doi.org/10.1520/STP163720200122)).
- GGI acquired Holo's assets in March 2024
  ([Tinicum](https://www.tinicum.com/business-Greene_Group_Industries.html);
  [Metal AM](https://www.metal-am.com/greene-group-industries-acquires-assets-of-holo/)). Under GGI, only stainless
  steel is advertised for PureForm, and copper no longer appears.

## Other vat-photopolymerization routes to metal parts

| Route | Who | Model | Metals | Notes |
|---|---|---|---|---|
| PureForm (film-fed DLP, MIM back end) | GGI (ex-Holo), California | Parts service | 17-4PH, 316 (copper under Holo) | Described above |
| Lithography-based Metal Manufacturing (LMM) | [Incus](https://www.incus3d.com/), Austria (founded 2019) | Sells printers (Hammer Evo35 for R&D, Pro25 for production) and its own feedstock, "standard and customized" | Steels, Ti, 99.9% Cu in production, precious metals ([Metal AM](https://www.metal-am.com/incus-is-expanding-its-material-portfolio-with-99-9-pure-copper/)) | Orthodontics is its biggest market ([3Dnatives, 2026](https://www.3dnatives.com/en/lithography-based-metal-manufacturing-incus-27042026/)). Fraunhofer IFAM has published LMM copper ([Metals 2024, doi:10.3390/met14111268](https://doi.org/10.3390/met14111268)) and Cu–Al₂O₃ dispersion-strengthened copper made by reducing Cu₂O, reaching 78% IACS ([Euro PM 2023, doi:10.59499/EP235765269](https://doi.org/10.59499/EP235765269)) |
| Admaflex DLP | Admatec Additive Solutions, Netherlands | Sells printers (Admaflex 130/300) | Ceramics, Cu, IN625, steel | Nano Dimension bought Admatec in 2022, closed it in 2025, and former management relaunched it mid-2025 ([Metal AM](https://www.metal-am.com/admatec-and-formatec-relaunch-following-nano-dimension-exit/)) |
| Hydrogel infusion AM (HIAM) | Caltech, Greer group | Academic | Cu, Ni, Ag, Co, Cu-Ni, W | Print a blank hydrogel, soak it in metal-salt solution, calcine to oxide, reduce in forming gas; ~40 µm features. The salt bath sets the composition, not a powder, but it works only for metals hydrogen can reduce, so not Al, Zr or Cr ([Nature 2022, doi:10.1038/s41586-022-05433-2](https://doi.org/10.1038/s41586-022-05433-2)) |
| Binder jetting (not VPP; for comparison) | ExOne with Ford; Desktop Metal with Uniformity Labs | — | Includes Al 6061 | The one sinter-based AM route I found with published near-full-density aluminum (~99%, 2021) ([SME](https://www.sme.org/technologies/articles/2021/march/exone-reports-breakthrough/); [MMS](https://mmsonline.com/news/desktop-metal-and-uniformity-labs-make-6061-aluminum-for-am)) |

## Fit with this lab

### Al-Zr and Al-Mn-Cr-Zr for LPBF (Phase I, ~80%): no

1. **Almost no precedent.** No vendor offers aluminum: not GGI (PureForm or MIM), not Incus, not Admatec. Holo said
   in 2021 that it planned aluminum, and no aluminum offering followed. The first web search missed the academic work
   that Edison's precedent search found. Zhang et al. printed polystyrene-coated AlSi10Mg at 45 vol% by DLP, debound
   it at 450 °C and sintered it at 600 °C in N₂ ([Addit. Manuf. 2021,
   doi:10.1016/j.addma.2021.101897](https://doi.org/10.1016/j.addma.2021.101897)). A 2025 paper does vat
   photopolymerization of Al alloys with radical inhibitors ([Adv. Eng. Mater.,
   doi:10.1002/adem.202500058](https://doi.org/10.1002/adem.202500058)), and a 2023 master's thesis measured cure
   depths of AlSi10Mg-filled resin but oxidized its parts in the furnace. Edison couldn't open either paper, so no
   final density, oxygen or strength is known. All of it is Al-Si-Mg casting alloy sintered in nitrogen, which is the
   Mg-and-nitrogen route described next. Every aluminum particle carries a stable oxide shell, and organic binder
   makes sintering harder still
   ([Fraunhofer](https://publica.fraunhofer.de/handle/publica/417479)). Press-and-sinter aluminum gets
   around this with Mg additions and a nitrogen atmosphere, and FLAIME counts Mg as a critical mineral to design out.
   Among AM routes, only binder jetting of 6061 has reached near-full density, and that needed special powder and
   furnace practice.
2. **Wrong microstructure.** The alloys are designed around LPBF rapid solidification. Zr and Mn are trapped in
   supersaturated solution, primary Al₃Zr seeds fine grains, and direct aging then precipitates nanoscale L1₂ Al₃Zr.
   Hours at sintering temperature would precipitate and coarsen those phases. A solution treatment can't put the Zr
   back, because its equilibrium solubility in Al tops out near 0.3 wt%. Alloy design for a sinter route would be a
   different problem.
3. **Wrong powder.** PureForm uses MIM-grade powder, which is much finer than the 15–63 µm LPBF cut that the rePOWDER
   campaigns target (d50 ≈ 65 µm reported for Al–10Cu). Fine aluminum also carries more oxide per gram and is a
   greater dust-explosion hazard.

### Cu-Cr-Zr complement (Phase I stretch, Phase II target): unproven, and the nearest precedent is discouraging

In favour:

- Copper is where PureForm started (Holo, >92% IACS), and GGI's MIM line already sinters pure copper.
- Sinter routes avoid copper's infrared reflectivity and fast heat conduction, which are the main difficulties in
  LPBF.
- Cu-Cr-Zr gets its strength from solution treatment, quench and aging, and those steps can follow sintering just as
  they follow casting. The alloy design carries over, which it does not for Al-Zr.
- MIM-grade feedstock exists. Sandvik markets Osprey C18150 (CuCrZr) powder developed for MIM and binder jetting
  ([Metal AM](https://www.metal-am.com/sandvik-launches-osprey-c18150-cucrzr-powder-for-high-temperature-applications/)).
- The proposal's Phase II targets (yield ≥200 MPa, ≥50% IACS; milestone table in
  `genesis-mission-proposal/flaime-genesis-proposal.tex`) are below what wrought, aged C18150 reaches. A sintered and
  aged part would not need to match wrought properties to meet them.

Against:

- Cr and Zr are the hardening elements, and both pick up oxygen and carbon. ZrO₂ won't reduce in hydrogen, and
  Cr₂O₃ needs very dry hydrogen at copper sintering temperatures. Oxygen and carbon left by the binder can therefore
  lock both elements up as oxides and carbides, which costs strength and conductivity. Even for pure copper, carbon
  is the main contaminant to avoid because it inhibits densification (Additive Manufacturing's 2021 profile of Holo).
- No one has published Cu-Cr-Zr made by vat photopolymerization. The closest work is Fraunhofer IFAM's LMM copper.
  That paper notes LMM copper has reached only ~90% density after 4 h at 1050 °C in hydrogen, against >99% for
  pressureless-sintered copper powder.
- The nearest alloy precedent is discouraging. A 2026 TU Wien thesis (Mastny, *High-strength copper alloys for
  indirect additive manufacturing using photolithography*) tried GRCop-42 (Cu-4Cr-2Nb at.%) for Incus LMM. The Cr₂Nb
  that strengthens it pinned the grain boundaries and stopped pressureless sintering, and silver or 90/10 bronze
  liquid-phase additives helped only partly. Trace water in the hydrogen oxidized the Nb and broke up the Cr₂Nb.
  Cu-Cr-Zr has less second phase than GRCop-42, but its Cr and Zr are just as easy to oxidize.
- Holo's >92% IACS for copper comes from a paper Holo co-wrote. Edison found no independent conductivity measurement
  for copper made this way.
- GGI doesn't list copper for PureForm today, so this would be a feedstock-development project. GGI's business is
  medical parts, not alloy R&D.

### Other overlaps

- **316H (Phase II).** PureForm's 316 is the only current material overlap with the roadmap. It is probably the
  low-carbon 316L in GGI's MIM list, though. 316H gets its creep strength from 0.04–0.10 wt% carbon, and MIM-style
  debinding works to keep carbon out.
- **Lab hardware.** For small, intricate stainless parts such as nozzles, fluid fittings or fixtures that need
  MIM-like detail without tooling, PureForm is a quote request away.
- **In-house back end.** BYU's CM hydrogen furnace (1600 °C; H₂ and N₂ atmospheres) is the right kind of furnace for
  sintering copper or stainless, so a VPP route's back end already exists on campus. Debinding residue can foul a
  hydrogen furnace, so check with its owner before running green parts in it.

### Formulation work on the OT-2

Asked on PR #229: could the OT-2 that [`digital-wetlab`](https://github.com/vertical-cloud-lab/digital-wetlab) uses
for precipitation experiments do formulation work for metal VPP? It fits hydrogel infusion best, because there the
metal comes from a salt bath. For powder slurries it can mix binders and act as a rough viscometer, but the tests
that decide whether a binder works happen off the deck.

**What the robot has** (digital-wetlab and byu-vcl records, October 2026):

- P300 and P20 single-channel GEN2 pipettes, and no 8-channel;
- a heater-shaker (37–95 °C), installed but not yet wired as of 10-21;
- the AS7341 colour-sensor tool, which the pipette picks up;
- an Ax optimization script and PHREEQC tooling.

It has no plate reader and no overhead camera yet, CB154 has no fume hood, and the lead-sulfide campaign
([digital-wetlab#80](https://github.com/vertical-cloud-lab/digital-wetlab/issues/80)) is next in line for the robot.
The lab has outsourced resin printing so far, and the BYU Prototyping Lab's Form 4s run only Formlabs resins.

1. **Hydrogel infusion (HIAM) baths: the best fit.** HIAM sets the composition with an aqueous salt bath, not with
   the resin. Making the baths means mixing concentrated salt solutions, which the wetlab already does, and holding
   them at 70 °C, which its heater-shaker can do.
   - *Published recipe.* Saccone et al. printed PEGDA-575 gels from a DMF-based resin, then washed them and exchanged
     them into water at 70 °C. They infused the gels with 2 M nitrates of Cu, Ni, Fe, Co or Ag, or with ammonium
     metatungstate, for 24 h at 70 °C. Then they calcined at 700 °C in air and reduced at 900 °C in forming gas
     ([Nature 2022](https://doi.org/10.1038/s41586-022-05433-2)). Linear shrinkage was 60–70%. The Cu and Cu-Ni parts
     were 93 and 86 wt% metal, the rest mostly carbon and aluminosilicate from the furnace tube.
   - *Open question.* The alloy doesn't come out in bath proportion: Saccone used a 1:1.21 Cu:Ni bath to get
     Cu50.5Ni49.5. A 2025 LLNL study found that the salt and the gel formulation both change part quality, and put
     that down to differences in how each cation infuses
     ([Inorg. Chem. Front., doi:10.1039/D5QI00139K](https://doi.org/10.1039/D5QI00139K)). I found no published map
     from bath composition to gel or alloy composition.
   - *An OT-2 campaign.*
     - Cast PEGDA disks in polypropylene wells (DMF attacks polystyrene) and cure them under a 405 nm flood lamp.
     - Run the washes on the heater-shaker.
     - Dispense mixed-nitrate baths over a design: Cu/Ni/Co/Fe fractions, total molarity, anion, temperature and
       time.
     - Read bath depletion on diluted aliquots with the colour sensor, after calibration. Co²⁺ absorbs near 510 nm,
       Ni²⁺ near 395 and 720 nm, and Cu²⁺ in the red and near infrared.
     - Check a subset by ICP-OES or XRF.
     - Calcine and reduce a subset, to check phase and composition. CuO and NiO from HIAM reduced fully at 350–400 °C
       in forming gas ([MS&T 2023](https://www.programmaster.org/PM/PM.nsf/ApprovedAbstracts/2D3434C8F121DA1985258A1B006F29D7)).

     Finding the bath recipe for a target alloy is then an inverse problem for the Ax loop. Start with Cu-Ni, so the
     1:1.21 point can be reproduced.
   - *Link to digital-wetlab's science.* Baths of 2 M mixed nitrates at 70 °C are concentrated mixed electrolytes.
     PHREEQC's `pitzer.dat` has no Cu, Ni, Co or nitrate (checked 2026-10-29), so these baths fall in the same kind
     of Pitzer gap as the sulfide brines.
   - *What it needs.*
     - PEGDA, a photoinitiator and an absorber. The published resin uses DMF and Michler's ketone, a reproductive
       toxicant and a carcinogen. An aqueous PEGDA resin with LAP and tartrazine would avoid both, but no one has
       tried it for HIAM.
     - The nitrates. Nickel and cobalt salts are carcinogens.
     - Sealed plates or capped vials that hold 70 °C for 24 h.
     - ICP-OES or XRF time.
     - Furnaces for both steps, with exhaust for the NOx that comes off during calcination. Nitrate-loaded gels can
       decompose violently if heated fast; Saccone ramped at 0.25 °C/min.
     - For printed lattices instead of cast disks, a 405 nm printer that accepts custom resin.
   - *FLAIME fit: low.* Hydrogen reduces Cu, Ni, Co, Fe, Ag and W, but Al, Zr, Cr and Mn stay as oxides. None of
     FLAIME's alloys can be made this way. The nearest copper variant is copper with oxide inclusions, which is
     dispersion strengthening, not the precipitation hardening Cu-Cr-Zr relies on. A 2025 Caltech thesis found that
     unreduced oxide nano-inclusions raised Cu-Ni hardness up to about four times
     ([Tran](https://thesis.library.caltech.edu/17290)). Its bibliography lists an ODS-by-HIAM paper whose status I
     couldn't find. This would link the two repos as a student-sized project, but it is not FLAIME work.
2. **Binders for powder slurries (PureForm, Incus): possible, but the tests that decide them are off the deck.**
   - *What the OT-2 can mix.* The low-viscosity parts: diluents and crosslinkers such as HDDA, TPGDA, IBOA, PEGDA and
     TMPTA (about 10–100 mPa·s), plus photoinitiator (TPO, BAPO), absorber, inhibitor, dispersant and porogen.
   - *What the OT-2 can measure.* An A*STAR group has shown how far the OT-2 goes with thick liquids:
     - It tuned OT-2 flow rates by Bayesian optimization for standards of 204–1275 cP
       ([Digital Discovery 2024, doi:10.1039/D3DD00255A](https://doi.org/10.1039/D3DD00255A)).
     - It used the OT-2 as a proxy viscometer for Newtonian fluids of 1.5–12 Pa·s
       ([2023, doi:10.1039/D2DD00126H](https://doi.org/10.1039/D2DD00126H)), and later for power-law fluids
       ([2025, doi:10.1039/D4DD00368C](https://doi.org/10.1039/D4DD00368C)).

     That range covers slurries at printable loading (18.7 Pa·s at 50 vol% Ti). With the powder mixed in off the
     deck, the OT-2 could screen viscosity against loading, binder and dispersant. Highly loaded slurries can have a
     yield stress, though, which those methods don't treat. The 2024 paper also used a P1000, while the lab has a P300
     and a P20.
   - *What it can't measure.*
     - Cure depth and critical dose, which need a windowpane test and a micrometer. The test is poorly standardized:
       in a 24-lab study, Dp varied up to 7× and Ec up to 70× between labs
       ([Addit. Manuf. 2024, doi:10.1016/j.addma.2024.104082](https://doi.org/10.1016/j.addma.2024.104082)). NIST
       released a working-curve reference resin, [RM 8047](https://www.nist.gov/node/1915556), in June 2026.
     - Carbon left after debinding, which needs TGA.
   - *What matters for Cu-Cr-Zr.* Which binder leaves the least carbon and oxygen to lock up Cr and Zr. TGA
     throughput, not dispensing, would set the pace.
3. **Lower value.**
   - Dispersant screens by settling at low loading could reuse the camera pipeline the lead work is building, but
     they only loosely predict rheology at printable loading.
   - Resins with the metal dissolved in them (metal acrylates, or nitrates in the monomer) could reuse the wetlab's
     precipitation-boundary imaging. HIAM was designed so the resin doesn't have to change with the metal.

The closest precedents involve no metals:

- The Allen and Gu groups at Toronto built a camera tool that the OT-2 picks up, and used it to image hydrogel
  formation in wells ([HardwareX 2025, doi:10.1016/j.ohx.2025.e00653](https://doi.org/10.1016/j.ohx.2025.e00653)).
- A Georgia Tech self-driving lab formulates photopolymers with a robot arm, liquid dispensing, and a powder
  dispenser for photoinitiators
  ([thesis](https://repository.gatech.edu/entities/publication/0f1b2235-375f-488f-bd67-4f6884473b7b)).

## Edison vetting (29 Oct 2026)

Five Edison tasks, asked on PR #229. Answers and full trajectories are in
[`edison-trajectories/vat-photopolymerization-metal-vetting/`](edison-trajectories/vat-photopolymerization-metal-vetting/):
commercial viability, process physics, comparison with other metal AM, funders named in paper acknowledgments
(LITERATURE_HIGH each), and a PRECEDENT search for aluminum and Cu-Cr-Zr. The answers lean heavily on one 2026 LMM
review of unclear venue (Segurola), Incus-affiliated papers and the TU Wien thesis, so treat them as a literature map,
not settled numbers. Edison also made mistakes: it placed GGI in Connecticut (GGI is in Oceanside, CA), called
Microlight3D a micro-LPBF vendor (it makes two-photon printers), and gave printer prices (€200–500k for Incus) and
MIM-versus-VPP part costs with no traceable source.

**Commercial outlook: a real but narrow niche.**

- Incus is the one active printer vendor. Holo's 2024 asset sale and Nano Dimension's 2025 exit from Admatec show
  that stand-alone metal-VPP businesses have struggled to reach scale. GGI's parts service survives inside a MIM
  company that already owns the debind-and-sinter back end.
- The niches it can hold: small (under ~50 mm), smooth, fine-featured parts in MIM alloys at 1 to ~10,000 pieces,
  below the volume where a $10–100k mold pays off. Examples are dental and orthodontic parts, surgical
  micro-instruments, watch and jewelry parts, connectors and nozzles. Copper cold plates and interconnects are
  another, because copper's reflectivity hurts LPBF.
- MIM wins above ~10,000 identical parts, and LPBF or binder jetting wins for parts larger than ~50–200 mm. LPBF wins
  wherever full density and flight or implant qualification matter.
- Maturity: about TRL 6–7, level with micro-LPBF and about one step behind binder jetting, which has a far larger
  installed base. Edison found no flight-qualified or FDA-cleared metal-VPP part. The key patent families are Trio
  Labs' (EP3419802B1, 2016 priority, powder and photocurable resin, then debind and sinter), ECN/Admatec's metal-
  precursor slurry (WO2017081160A1) and Caltech's hydrogel-infusion family (US20220314183A1). Freedom to operate
  would need counsel.

**Process physics: what holds up.**

- Curing is the bottleneck. Metal particles absorb and scatter, so cure depth collapses as loading rises. Raw
  titanium at 45 vol% cured under ~30 µm, barely one layer, until the powder was coated to cut the refractive-index
  mismatch. Typical LMM layers are 20–50 µm. Liquid slurries top out around 45–50 vol%, above which viscosity
  (18.7 Pa·s at 50 vol% Ti) pulls on the release film. Incus avoids settling with a binder that is solid at room
  temperature and is spread hot.
- Debinding sets the wall limit. Crosslinked acrylate doesn't melt or dissolve out the way a MIM binder does, so
  thick sections crack or blister. GGI's 3.5 mm maximum wall fits that physics, but no one has checked it
  independently, and neither has anyone checked Incus's ~10 mm.
- Shrinkage is about 20% linear, close to isotropic in Incus's reports, within MIM's 15–25%.
- Properties: µDLP 316L reached ~99% density (by image analysis), 187–194 MPa yield, 534–579 MPa UTS and 51–76%
  elongation, above the MPIF 35 minima and close to binder-jetted 316L. As-sintered Ra under 2 µm is supported.
- Carbon is the recurring problem. Incus's Ti-6Al-4V carries 0.11 wt% C, against 0.08 wt% allowed for medical grade.
  NiTi showed the same carbon sensitivity.
- Vendor claims with no independent data: Holo's >92% IACS copper; GGI's 0.07 mm wall, 3.5 mm maximum wall,
  ±0.025 mm to 12 mm and 0.8–1.6 µm Ra; Incus's 99.9% copper conductivity and ~10 mm wall; and any fatigue data for
  this route. The Incus-affiliated tolerance is ±0.5%, looser than GGI's ±0.025 mm.

**Compared with other metal AM (Edison's table, rounded; vendor figures marked there):**

| Route | Smallest wall | As-built Ra (µm) | Density (%) | Part scale | Main advantage over metal VPP |
|---|---|---|---|---|---|
| Metal VPP (PureForm, Incus) | ~70 µm (vendor) | <2 | ~95–99 | ≤50–200 mm | — |
| Standard LPBF | ~150–300 µm | 5–15 | >99.5 | up to ~800 mm | Full density, qualification heritage, alloy range incl. Al |
| Micro-LPBF | ~40–60 µm | 1.3–5 | >99 | <100 mm | No debind or sinter chain |
| Binder jetting | ~300–500 µm | ~6 | 95–97 (>99 with HIP) | ~400–800 mm beds | 50–200 cm³/h, larger parts, bigger installed base |
| Bound-metal FFF | ~0.5–1 mm | 5–15 | ~95–99 | ≤300–500 mm | Cheap machines |
| MIM | ~50–100 µm (micro-MIM) | 0.4–1.6 | 95–98 | <200 g usual | Unit cost at volume (seconds per part) |
| Two-photon / HIAM | 35–250 nm | — | ~80–99 | <1 mm | Resolution, three orders of magnitude finer |

## Who funds it: US federal awards

Searched on 29 Oct 2026 in two passes. The first went through the atomizer panel Pi's headed Chromium, driven by
mouse and keyboard events (`scripts/pi_browser.py`, `scripts/pi_grant_search.py`):

- **NSF:** 30 phrase queries through NSF's award API (851 unique awards).
- **NIH RePORTER:** one Boolean query, 64 projects, none of which make metal parts.
- **USAspending:** grants and contracts for eight phrases, 149 awards.
- **SBIR.gov:** its own award search.

SBIR.gov's search box misses most matches, so `scripts/sbir_metal_vpp_screen.py` also screened SBIR.gov's full award
file (219,770 awards with abstracts, downloaded on the runner). It kept awards that pair a photopolymerization term
with a metal term, 85 in all, and each was read by hand.

The second pass filled the first one's gaps (`scripts/federal_dump_screen.py`, and `pams` in
`scripts/pi_grant_search.py`):

- **NASA TechPort:** its project API ignores the search term and returns all 21,162 projects (~115 MB) at once. That is
  what froze the 1 GB Pi in the first pass. The runner screened the whole dump with the same terms (17 hits, read by
  hand), and TechPort lists each project's NASA contacts.
- **ARPA-E:** all 1,729 projects, through the full-text index behind the site's search page. None mentions
  stereolithography, photopolymer(ization), photocurable resin, DLP, hydrogel or metal injection.
- **DOE Office of Science (PAMS):** award-number and abstract-keyword searches over all award statuses, in the Pi's
  Chromium. PAMS gives the program manager on each award's public abstract.
- **OSTI.gov:** 19 queries, 720 DOE-sponsored records, screened the same way. Their contract numbers name the funding
  office.
- **Paper acknowledgments (OpenAlex):** 20 queries, 2,697 papers, 102 with a metal-VPP title, checked for US funders.
  This is the way to find DoD basic-research grants, which USAspending describes too vaguely to find by keyword.

Only awards that end in a metal part are listed. Sinter-based metal VPP (metal powder in a photopolymer, debound and
sintered):

| Agency, program | Award | Years | Recipient | PI | Program officer | Amount | Work |
|---|---|---|---|---|---|---|---|
| NSF ENG/CMMI, Advanced Manufacturing + CAREER | [2236894](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2236894) | 2023–28 | Michigan State University | Haseung Chung | Janis Terpenny | $567,121 | DLP of photopolymer and metal-powder mixtures of tunable viscosity, then debind and sinter, for large-area, high-speed metal AM. The only on-topic federal research grant found. Its first paper is on dispersants for metal–photopolymer slurries (*J. Manuf. Mater. Process.* 2025) |
| NSF ENG/CMMI, Major Research Instrumentation | [2511215](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2511215) | 2026–29 | University of Texas at El Paso | Alexis Maurel (four co-PIs) | Lesley Sneed | $715,278 | Buys a multi-material VPP printer for polymers, ceramics and metals, "only the third in North America" |
| NASA SBIR, topic Z6.01 | NNX15CP38P (I), NNX16CP82C (II); TechPort [33603](https://techport.nasa.gov/projects/33603), [92583](https://techport.nasa.gov/projects/92583) | Jun–Dec 2015; Sep 2016–Sep 2018 | AlphaSense, Inc., Wilmington, DE | Pengcheng Lv | Technical monitor at JPL, the supporting center (named in TechPort). TechPort lists Jason L. Kessler and Carlos Torrez as the SBIR/STTR program's director and manager, which may be current rather than 2015 staff | $118,395 + $748,536 | DLP of slurries of metal particles in photocurable resin, to make green parts for gradient metal alloys. AlphaSense's other ~30 SBIRs are mostly sensors, and no follow-on metal-AM award was found |
| Air Force SBIR I | — | 1996 | Ceramic Composites, Inc., Annapolis, MD | Walter Zimbeck | — | $96,943 | Freeform fabrication of tungsten absorber/thruster parts. The abstract doesn't name the process; the same PI's next two awards are stereolithography |
| DARPA SBIR I | — | 1997 | Ceramic Composites, Inc. | Walter Zimbeck | — | $98,926 | Visible-light stereolithography of metal foams with designed porosity |
| MDA SBIR I | — | 1998 | Ceramic Composites, Inc. | Walter Zimbeck | — | $69,991 | Photocurable rhenium resins for stereolithography of hot-gas valve bodies |

Photopolymer-template and salt-infusion routes that end in metal, and adjacent work:

| Agency, program | Award | Recipient | PI | Program officer | Work |
|---|---|---|---|---|---|
| DOE Office of Science, BES Materials Sciences and Engineering (CFDA 81.049) | DE-SC0016945, 2016–24, $1,409,478 (USAspending) | Caltech | Julia R. Greer | John Vetrano, Mechanical Behavior and Radiation Effects (PAMS) | A core grant on small-scale metal mechanics, first titled for nano-sized metallic glasses. The 2023–24 renewal, *New Deformation Mechanisms in Nanocrystalline Nano-porous Small Scale Metals*, proposes AM of sub-micron Ni and Cu outright, and its final report covers hydrogel-infusion nickel nanopillars made by two-photon lithography ([OSTI 2571089](https://www.osti.gov/biblio/2571089)). Acknowledged by the 2022 *Nature* hydrogel-infusion paper (Cu, Ni, Ag, Cu-Ni), the 2025 Cu–Ni follow-up in *Small* and a 2026 *Nat. Rev. Mater.* review. PAMS lists it inactive after seven support periods. Edison ranks it the largest single public funder of metal-photopolymer work |
| NASA STMD, Space Technology Research Grants | TechPort [183708](https://techport.nasa.gov/projects/183708), 2025–29 | Caltech | not listed (a Caltech co-investigator is) | Technical monitor Christopher J. Wohl (Langley); program director Matthew C. Deans, program manager Hung D. Nguyen | *Micro-Architected Metallic Lattices for Lunar Dust Mitigation*: hydrogel-infusion lattices of alloys and refractory metals, 100 nm to 50 µm features, TRL 2 to 3. The one active federal award found whose own abstract names a photopolymer-to-metal process, besides the two NSF awards above |
| NASA STMD, Space Technology Research Grants | TechPort [95502](https://techport.nasa.gov/projects/95502), 2018–21 | UC Irvine, with HRL Laboratories | Lorenzo Valdevit | Technical monitor Brett A. Bednarcyk (Glenn) | Ceramic (SiOC) and hollow metallic truss-core lattices grown from self-propagating photopolymer waveguides, for large space structures |
| DoD (award not given in the paper's metadata); INL; UT System | — | UTEP | Alexis Maurel's group | — | Compositionally graded W–Ni lattices by "ionic solution-enabled" VPP (*Addit. Manuf. Lett.* 2026). The group's earlier VPP copper current collectors were printed, soaked in a precursor solution and fired (*Adv. Manuf.* 2024, with Sandia and ORNL co-authors under their DOE operating contracts). Same PI as the NSF MRI above |
| ONR MURI | N00014-24-1-2313, 2024–27, $3,750,000 | Penn State (lead) | — | — | *Photochemical and Photothermal Additive Manufacturing of Preceramic Polymers*. Acknowledged by Michigan State's hydrogel-infusion carbides of Ti, Mo and W (*ACS Materials Lett.* 2025). Carbides, not metals |
| NIH NCI R01; ARPA-E IDEAS | R01CA194533 (UCSF, endovascular chemofiltration); DE-AR0000884 (Caltech, *Nanomechanics of Electrodeposited Li*, 2017–18, $290,000) | Caltech | Julia R. Greer and co-inventors | NCI: Pushpa Tandon | The government-interest statement of Caltech's US 11,318,435 (2018 priority): a photopolymerized metal-salt hydrogel, then heat treatment in an atmosphere that sets the composition. Neither grant was for metal AM, so the support is incidental |
| ONR; ARO; NIH | N00014-17-1-2977; W911NF1510548; NIH grants including 1R01EB024261 | MIT | Edward S. Boyden | — | Implosion fabrication, *Science* 2018: silver deposited in a photopatterned hydrogel, then shrunk. A DOE Office of Science SBIR (DE-SC0021593, Irradiant Technologies, Cambridge, MA; PI Daniel Oran; PM Claudia Cantoni) develops line-scan temporal focusing and implosion-fabrication lithography |
| NSF CMMI Advanced Manufacturing, EAGER | [2528559](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2528559), 2025–27, $99,105 | NC State | Henry Oliver Ware | Janis Terpenny | DLP with acoustically aligned fillers sintered in place by intense pulsed light, for composite electrodes |
| NSF CMMI Advanced Manufacturing, CAREER | [2542270](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2542270), 2026–31, $549,994 | University of Connecticut | SeungYeon Kang | Janis Terpenny | One-step DLP printing of micro- and sub-micron conductors ("3D OHMIC") |
| NSF CMMI, CAREER | [2338752](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2338752), 2024–29, $600,857 | Arizona State | Xiangjia Li | Janis Terpenny | Electrically assisted printing of metal patterns inside polymer parts. The same PI holds a patent on DLP of CuSO₄ photoresin reduced to copper (US20250222650A1); Edison found no government-interest statement in it |
| DOE NNSA (LLNL and LANL operating contracts) | — | LLNL; LANL | (national-lab staff, not named here) | — | LLNL: hollow Ni-P metamaterials on large-area projection-microstereolithography templates (*Nat. Mater.* 2016) and precursor design for hydrogel-infusion ceramics including CuO (*Inorg. Chem. Front.* 2025). LANL: a 2020 talk on binder-jet and DLP options for ceramics and porous metals ([OSTI 1711365](https://www.osti.gov/biblio/1711365)), and a 2026 study of nickel content in VPP tungsten lists LANL as funder |

What this adds up to:

- **No federal program targets metal VPP.** The money is one NSF CAREER award, three 1990s DoD SBIRs and one NASA
  SBIR, none of which led to a product. The rest is basic-science and space-technology grants (DOE BES, NASA STRG,
  ONR, ARO, NIH, DoD) that support photopolymer-template and salt-infusion routes as a side line.
- **Program officers.**
  - NSF: Janis Terpenny (CMMI, Advanced Manufacturing) oversees four of the five NSF awards above, including the
    Michigan State CAREER award, and Lesley Sneed handled the UTEP MRI. Earlier NSF awards on VPP composites with metal
    flakes or particles (USC, 2016–17) went through Khershed Cooper and Steve Schmid.
  - DOE: John Vetrano (BES, Mechanical Behavior and Radiation Effects) managed DE-SC0016945, the grant behind
    hydrogel infusion.
  - NASA: the AlphaSense SBIR had a JPL technical monitor. The Caltech hydrogel-infusion grant sits in Space Technology
    Research Grants (program director Matthew C. Deans, program manager Hung D. Nguyen), monitored from Langley.
- **The companies.** Holo, GGI, Incus, Admatec, Tethon 3D and Trio Labs have no SBIR/STTR awards in SBIR.gov's full
  file. Edison found no government-interest statement on Holo's patents (US10245785B2 and family), so Holo was
  venture funded. Abroad, Fraunhofer's LMM copper work was funded by the EU's ERDF (AddiMet project, 100405446). The
  TU Wien Incus-printer thesis names no public funder.
- **Searched with nothing on-topic found:**
  - NIH.
  - DOE EERE, whose closest award is ceramic (DE-EE0010216 to GE, photopolymerization AM of fiber-reinforced SiC,
    2022, $968,825).
  - NIST, whose closest is a $50k grant on ceramic-filled VPP defects to Colorado School of Mines.
  - DoD contracts, which were stereolithography equipment, resin and maintenance, plus an ONR grant for ceramic
    stereolithography casting molds.
  - ARPA-E. Its nearest projects are GE's lithographically printed ceramic cores and shells for single-crystal
    turbine-blade casting (OPEN 2021, $2,696,056), and Georgia Tech's extruded iron-oxide lattices reduced to steel in
    hydrogen (ROSIE, 2023, $2,843,195).
  - PAMS abstracts: "stereolithography" 1 hit, "photopolymer" 3 and "two-photon lithography" 1 (the Irradiant SBIR).
    "Digital light processing", "vat photopolymerization" and "hydrogel infusion" found nothing.
  - NASA's other TechPort hits: copper and nickel plated onto SLA parts (Sears Scientific SBIR, 2021), and Goddard's
    micro-AM (Center Innovation Fund, 2015–17), which replicated polymer templates in refractory ceramics by CVD.
- **DTIC, only partly.** On 29 Oct 2026 DTIC's own search was offline ("offline while we enhance the capability"),
  and its report server (`apps.dtic.mil`) answered with a maintenance page, even from the Pi; from the runner it
  returns HTTP 403. The results page falls back to a Google site search, and eight metal-VPP queries through it, in the
  Pi's Chromium, found only AM overviews. One hit, ADB195810 (a 1990s limited-distribution report, since released),
  has a snippet that pairs stereolithography with tungsten, nickel aluminides, MoSi₂ and copper. It may be the
  Ceramic Composites SBIR work above, but the PDF couldn't be opened. Rerun when DTIC is back.

## Questions for Greene Group, if Cu-Cr-Zr moves forward

1. Does Holo's copper PureForm process still run, and what density and conductivity do copper parts reach now?
2. Would GGI print a customer-supplied powder, such as Sandvik's MIM-grade C18150 or the fines from a BYU rePOWDER
   Cu-Cr-Zr run? What particle size distribution and quantity would it need?
3. What carbon and oxygen levels do sintered copper parts end up with, and in what sintering atmosphere?
4. What are the H200's build area and largest part size? What would a small batch of test coupons cost (flat
   tensile and conductivity bars, ≤3.5 mm thick)?
