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
- **Fit for FLAIME's aluminum alloys: none.** No vendor of this kind of process offers aluminum, and a web search found
  no published vat-photopolymerization work on any aluminum alloy. The usual way to make aluminum sinter is a Mg
  addition, and Mg is one of the minerals FLAIME's alloys are designed to avoid. Even if the process worked, hours at
  sintering temperature would undo the rapid-solidification supersaturation that the Al-Zr and Al-Mn-Cr-Zr designs
  depend on.
- **Fit for the Cu-Cr-Zr complement: plausible, unproven, and worth one conversation in Phase II.** PureForm started
  as a pure-copper process (>92% IACS). GGI's MIM line already sinters copper. Cu-Cr-Zr is a solution-treat-and-age
  alloy, so its hardening survives a sinter route, and MIM-grade C18150 powder is on the market. Nobody has published
  Cu-Cr-Zr made this way, though, and GGI doesn't list copper for PureForm today.

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

1. **No precedent.** No vendor offers aluminum: not GGI (PureForm or MIM), not Incus, not Admatec. Holo said in 2021
   that it planned aluminum, and no aluminum offering followed. A web search found no published
   vat-photopolymerization of any aluminum alloy, only alumina ceramics and a cure-depth study of Al powder in HDDA
   resin. Every aluminum particle carries a stable oxide shell, and organic binder makes sintering harder still
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

### Cu-Cr-Zr complement (Phase I stretch, Phase II target): plausible, unproven

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

## Questions for Greene Group, if Cu-Cr-Zr moves forward

1. Does Holo's copper PureForm process still run, and what density and conductivity do copper parts reach now?
2. Would GGI print a customer-supplied powder, such as Sandvik's MIM-grade C18150 or the fines from a BYU rePOWDER
   Cu-Cr-Zr run? What particle size distribution and quantity would it need?
3. What carbon and oxygen levels do sintered copper parts end up with, and in what sintering atmosphere?
4. What are the H200's build area and largest part size? What would a small batch of test coupons cost (flat
   tensile and conductivity bars, ≤3.5 mm thick)?
