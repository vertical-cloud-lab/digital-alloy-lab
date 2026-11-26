# Patent survey: aluminium alloys for LPBF and rapid-solidification powder

Compiled 2026-11-26 in about 35 minutes of web research. All compositions are in wt% unless marked otherwise.

## How to read the "verified?" column

- **page**: I fetched the Google Patents page (or the patent PDF from patentimages) myself and read the numbers there.
- **page\***: the numbers were read off the Google Patents page by a research sub-agent I delegated to in the same session. I did not re-open those pages myself. Treat them as one step weaker than `page`.
- **search-snippet**: the numbers come only from search results.
- **unverified**: neither of the above.

Caveats that apply throughout:

- Google Patents "status" and "expiry" fields are Google's own assumption, not a legal status. I give them as shown.
- Google Patents pages are long, and WebFetch reads only the first ~100k characters. For several patents the claims or example tables were cut off or garbled, and each such case is flagged.
- Product-name mappings (for example "RS-553 = EP3903964") are my inference unless stated otherwise. None of the patents names the commercial product.

---

## 1. Summary table

| # | Assignee (product) | Number(s) and URL | Priority / status | Independent-claim ranges (wt%) | Key worked examples and properties | Mechanism | Process info | verified? |
|---|---|---|---|---|---|---|---|---|
| 1 | EADS Deutschland, now APWORKS / Airbus (Scalmalloy precursor) | DE102007018123B4 (A1), WO2008125092A1. [link](https://patents.google.com/patent/DE102007018123A1/en) | 2007; granted, active, expires about 2027-04 | Claim 1 is any Al-Sc alloy built by laser/beam AM (no numbers). Dependent claims: Sc ≥0.4 (0.41–2.0; 0.8–1.4); Mg 2–10 (3–6; 4–5); optional Zn, Cu, Mn, Si, Li, Ag, Fe 0.05–2.0 each; Zr, Ti, Ta, Hf, Y, Er ≤2 each, ≤3 total | Wire AlMg4.6Sc1.4, laser wire deposition. As built: YS 257, UTS 346 MPa, A5 12%. After 300 °C/5 h: YS 400, UTS 450 MPa, A5 5%. Porosity 5–10% | Al3Sc supersaturation by fast cooling (>100 K/s), then precipitation | 3 kW Nd:YAG, wire feed 7 m/min. Ageing 100–400 °C (250–400 preferred) | page |
| 2 | Airbus Defence and Space (Scalmalloy powder) | US11433489B2 (US2017/0165795), EP15199831. [link](https://patents.google.com/patent/US11433489B2/en) | 2015; active (adj. expiry 2039) | Mg 0.5–10; Sc 0.6–30; Zr 0.05–1.5; Mn 0.01–1.5; Zn 0.2–1.0; Ti 0.01–0.2; Ce ≤0.25; Si ≤0.25; Fe ≤0.25; Hf ≤0.5; Be ≤0.004; B ≤0.008; listed others ≤0.5 total. Requires primary Al3(Sc1-xZrx) ≤20 µm | No worked examples on the page | Primary Al3(Sc,Zr) particles plus precipitation | Melt ≥700 °C (≥800 preferred). Cooling >10 K/s up to 5×10^7 K/s (He gas). Reheat 100–400 °C (225–350 preferred). No LPBF numbers | page |
| 3 | Airbus Defence and Space / Airbus SAS | US20220168811A1, EP4008457A1. [link](https://patents.google.com/patent/US20220168811A1/en) | 2020; US **abandoned** 2025 | Ti 0.1–15; Sc 0.1–3; Zr 0.1–3; balance Al | Al-1Ti-0.75Sc-0.35Zr. Variants: Ti 3–15; +2V; +1.2Ni; +1V+2Cr with 5Ti. **No properties reported** | Al3(Sc,Zr,Ti) | Melt-spun about 10^6 K/s, flakes. Ageing 250–450 °C (325–350 preferred) | page |
| 4 | HRL Laboratories (7A77-type, Zr-functionalised 7075) | US11286543B2 (CIP of US11053571B2). [link](https://patents.google.com/patent/US11286543B2/en) | 2017; active (adj. expiry 2039) | Claim 1 (read from PDF): Al 84.5–92.1; Cu 1.1–2.1; Mg 1.8–2.9; Zn 4.5–6.1; Zr 0.5–2.8 present as nano/micro particles or inclusions, uniformly distributed. Dependent claims: Si, Fe 0.005–0.4; Mn 0.005–0.3; Cr 0.005–0.1 | 7075 + Zr (T6) and 6061 + Zr. Tensile curves only in figures, so **no numbers in the text** | Heterogeneous nucleation on Zr/Al3Zr gives equiaxed grains and suppresses hot cracking | Concept Laser M2, 400 W fibre laser, ≤7.9 m/s, 50 µm spot, layer 20–80 µm | page (claim 1 from PDF) |
| 5 | HRL Laboratories | US11053571B2 "Aluminum with grain refiners". [link](https://patents.google.com/patent/US11053571B2/en) | 2017; active | Claims not read (page truncated). Summary: Al ≥90 plus grain-refining nanoparticles ≥0.01 vol% (Zr, Ta, Nb, Ti, or their compounds) | Pure Al + Ta; 7075 + Zr; 6061 + Zr (figures only) | Nucleant nanoparticles | — | page (summary only) |
| 6 | HRL Laboratories | US10960497B2 (welding filler). [link](https://patents.google.com/patent/US10960497B2/en) | 2017; active | Claims not read. Summary: metal particles 10–99.99% plus nanoparticles 0.01–10% | ZrH2-functionalised 7075 shows no hot cracking in a multipass weld | Nucleant | — | page (summary only) |
| 7 | HRL Laboratories | US12421576B2 "Aluminum-chromium-zirconium alloys". [link](https://patents.google.com/patent/US12421576B2/en) | 2017; granted 2025, active | Claims not read. Description: Cr and/or Zr ≥0.1 at%; Zr/Cr 0.1–10 | Al-2Cr-1Zr: UTS about 263 MPa as built, 337 MPa after 350 °C/32 h. Al-2Cr-2Zr: 325 MPa after 350 °C/32 h. Al-0.5Cr-0.5Zr, Al-1Cr-1Zr, Al-1Cr-2Zr, Al-4Zr in figures only. The page labels these at% in one place and wt% in another | Al3Zr nucleation plus Cr/Zr precipitation | Concept Laser M2, Ar. Preheat may go up to 50 °C below the solidus | page |
| 8 | Aeromet International (A20X / A205) | GB2477744B. [link](https://patents.google.com/patent/GB2477744B/en) | 2010; active per Google, expires 2030 | Claims **not on the page**. A UK IPO opinion (search result) describes an Al-Cu casting alloy with free Ti and insoluble TiB2 interdendritically, Ag 0–1.5 in claim 1 | — | TiB2 plus free-Ti grain refinement | — | search-snippet. I could not confirm the link to A20X on the page |
| 9 | QuesTek Innovations | US10941473B2 "Aluminum alloys". [link](https://patents.google.com/patent/US10941473B2/en) | 2015; active (expiry about 2037) | Claim 1 (AM alloy): Zn 3–9; Mg 3–6; Cu 1–2; Zr 0–1; Y, Er, Yb, Ag, Mn 0–2 each. Claim 12: Zn 4–9, Mg 0.5–2, Cu ≤0.5, Zr 0.5–1. Claim 19: Zn 3–9, Mg 0.5–2, Zr 0.5–2, Er 1–2, Cu <0.5, Sc <0.01. Claims 13–14: Al-3.1Mg-2Ag-0.5Cu-0.1Zr-0.4(Yb+Er or Y) | HV in T7, all crack-free: Al-6.3Zn-3.2Mg-1.1Cu-0.1Zr 183; Al-7.5Zn-4.6Mg-1.5Cu-0.1Zr 184; Al-3.3Zn-5.5Mg-1.4Cu-0.1Zr 168. References: 7050-T7 172 (cracked); AlSi10Mg-T6 105. No tensile data | About 10% soluble eutectic backfills cracks, then dissolves in post-processing. Solidification range ≤170 °C | EOS M280. Alloy 4: Ar-atomised 20–63 µm (200 kg). Solution 480 °C/1 h, age 177 °C | page |
| 10 | NanoAL LLC (Addalloy; Northwestern-origin technology) | US11603583B2, WO2018009359A1. [link](https://patents.google.com/patent/US11603583B2/en) | 2016; active per Google (expiry about 2037). Some search results call the WO "ceased" | Claim 1 (AM method): Mg about 1–10; Zr about 0.30–3; Sc ≤0.05 (impurity only); only unavoidable Zn, Cu, Si. Claim 14 adds a single-step heat treatment at 350–450 °C for 0.5–24 h. Claim 3: +0.3–1.5 of Ti, Hf, V, Nb or Ta. Claim 13: Al-3.6Mg-1.2Zr or Al-4Mg-1.7Zr | LPBF Al-3.6Mg-1.2Zr: hardness and yield **in figures only**. The text claims the best yield/ductility among commercial AM alloys after peak ageing at 400 °C/8 h. Melt-spun Al-4Mg-0.7Zr and Al-4Mg-1.7Zr compared with Al-4Mg-0.8Sc | Zr replaces Sc. Primary Al3Zr nucleates fine grains; L1₂ Al3Zr ageing at about 400–425 °C | **Melt-spinning casting temperature >1100 °C for the Zr melts**. Extrusion up to about 450 °C | page |
| 11 | C-TEC Constellium (Aheadd CP1-type Al-Fe-Zr) | US12377463B2, WO2020/…(PCT/FR2020/050108). [link](https://patents.google.com/patent/US12377463B2/en) | 2019; granted 2025, active | Claim 1 (powder): Zr 0.5–2.5; Fe 0.5–2.5; Si ≤0.3; Cu ≤0.5; Mg ≤0.2; others <0.1 each, <0.5 total. Claim 2 covers CSC, LMD, AFS, FAST, IRFW products. Claim 3 (method) was truncated on the page | Z-direction tensile (YS/UTS MPa/A%): **Al-1.52Zr** 109/148/22 as built, 235/266/8.6 after 400 °C/4 h. **Al-1.78Zr-1.04Fe** 214/240/16.8 as built, 298/307/7.8 after 400 °C/1 h. **Al-1.23Zr-0.94Fe** 133/198/26.2 as built, 299/309/15.1 after 400 °C/4 h. **Al-0.81Zr-1.83Fe** 118/215/18.1 as built, 278/316/18.8 after 400 °C/4 h. **Al-1.39Zr-0.32Cu** 153/193/27.5 as built, 279/304/18.6 after 400 °C/1 h. Conductivity 18–33 MS/m | Al3Zr nucleation plus precipitation; Fe eutectic | EOS M290, 370 W, 1250–1400 mm/s, hatch 0.11 mm, 60 µm layer. **Plate about 200 °C** (25–150 °C also processable). Stress relief 300 °C/4 h. Notes that Mg evaporates during atomisation and SLM | page |
| 12 | C-TEC Constellium | US11692240B2 (FR1871133). [link](https://patents.google.com/patent/US11692240B2/en) | 2018; granted 2023, active | Claim 1 (process): Fe 1–3.7; Zr, Hf, Er, Sc, Ti 0.5–4 each, ≤4 total; Si 0–4; V 0–4; no Cu and/or Mg ≤0.5 | Al-1.7Si-3.5Fe-1.3V-3Zr (Innov4), Z-direction: 372/410 MPa/6.7% after 300 °C/2 h; 432/467/4.8% after a further 400 °C/1 h; 230/249 MPa at 200 °C. HK0.05 for Zr 1/2/3 variants: 172/187/199 as built | Fe/V/Si dispersoids plus Al3Zr | Form Up 350, 370 W, 1000–1400 mm/s, 60 µm, **plate 200 °C** (50–300 beneficial). VIGA powder | page |
| 13 | C-TEC Constellium | US12378641B2. [link](https://patents.google.com/patent/US12378641B2/en) | 2018; granted 2025, active | Fe 2–8; optional Zr 0.5–2.5 (or <0.5); Si <1; Cu ≤0.5; Mg ≤0.2; others <0.1 each | **Binary Al-4Fe**: 282/405 MPa/4.5% as built; 262/378/7.4% after 400 °C/1 h; 152/303/22% after 400 °C/100 h. Conductivity 24.6–29.8 MS/m. Liquidus about 660 °C | Fine Al-Fe eutectic | EOS M290, 370 W, 1400 mm/s, 0.11 mm, 60 µm, **plate 200 °C**. Stress relief 300 °C/4 h | page |
| 14 | C-TEC Constellium | US12037661B2 and EP3622095B1 (same 2017 family). [US](https://patents.google.com/patent/US12037661B2/en), [EP](https://patents.google.com/patent/EP3622095B1/en) | 2017; granted, active | US: Si 4–15; Fe 2–15; V 0.1–5; Mn 0.1–2 (± a long list of optional elements). As built Hv0.1 ≥160. EP claim 1: Si 4–20, Fe 2–15 plus optional Mn, Ti, V, Zr, Cr, Mg, Ni, Ce etc. | Al-6.8Si-8.2Fe-0.19Mn-1.1V: 181 Hv0.1, against 158 for 8009. No tensile data | Fe-V-Si dispersoids | 400 W Nd:YAG. Window E > 0.2V − 35. Powder made by blending 8009 powder with Si powder | page |
| 15 | C-TEC Constellium (Aheadd HT1-type Al-Mn-Ni-Cu-Zr) | US20230191488A1, WO2021156582, EP4149703B1. [link](https://patents.google.com/patent/US20230191488A1/en) | 2020; US **abandoned**, EP granted | Zr 0.60–1.40; Mn 2–5; Ni 1–5; Cu 1–5. Claim 2 lets Ti, V, Sc, Hf, Er etc. partly replace Zr | Al-3.77Mn-2.77Ni-1.90Cu-1.02Zr: YS 303 MPa after 300 °C/4 h, 420 MPa after 400 °C/1 h; 270 MPa at 200 °C. Alloy with 1.53Zr: 372 MPa. Low-Zr alloys 184–267 MPa. No UTS or elongation | Mn solid solution, Ni/Cu eutectic, Al3Zr | EOS M290, 370 W, 1400 mm/s, 60 µm, plate 100–200 °C | page\* |
| 16 | Fehrmann (AlMgty-type) | US12281374B2, EP3732310A1. [link](https://patents.google.com/patent/US12281374B2/en) | 2017; granted 2025, active | Mg 9–14; Ti 0.15–1; B 0.0009–0.2; Be 0.001–0.1; Mn 0.0001–0.1; Fe ≤0.1; Si ≤1; Cu, Zn ≤0.01; Sc ≤0.05 | **Castings only**: Al-10.9Mg-0.30Ti-0.005B-0.015Be permanent mould, 400/202 MPa/25% after 450 °C/24 h. Al-10.0Mg sand cast, 320/172/12% after 430 °C/9 h | Ti-B grain refinement; Be protects Mg; heat-treatment phase change (hypothesis) | Melt 650–800 °C; inert-gas atomisation (de Laval nozzle); powder 20–65 µm. No LPBF parameters | page\* |
| 17 | AMAG Casting + Audi | US11597984B2, EP3607103B1, WO2018185259A1. [link](https://patents.google.com/patent/CA3059286A1/en) | 2017; granted | Fe 0.5–1.5 and Mn ≤0.9 with a Mn/Fe relation (garbled on the page). Optional Sc/Er 0.1–2, Li 0.1–3, Ni ≤2, Cr/Ti/V/Zr etc. ≤1. Dependent claims: Al-Mg (Mg 2–7), Al-Mg-Si, Al-Zn (Zn 1–8, Mg 1–3), Al-Si | SLM UTS/A: Al-Mg type 370 MPa/19.5%, 105 HV3 (cracks <30 µm vs >400 µm in the reference). Al-Zn type 595 MPa/11.5%. Al-Si type 480 MPa/14%. **Composition columns garbled**, so the exact compositions are unconfirmed | Primary Fe/Mn phase forms before Al and refines the structure against hot cracking | Nd:YAG 200–400 W, 250 mm/s, 30 µm, 135 µm hatch | page\* (compositions unconfirmed) |
| 18 | Elementum 3D (RAM) | US10507638B2; US11802321B2; US12116652B2. [link](https://patents.google.com/patent/US11802321B2/en) | 2015; active | Claim 1: Al-alloy powder blended with a nucleant (or a precursor reacting in situ). **No numeric ranges** | Al 76.8 + Ti 16.8 + B4C 6.5 → Al + TiB2 + TiC, 62.9 HRB. Al-4.5Mg + Ti-6Al-4V + B4C, 90.4 HRB | In-situ ceramic nucleants | EOS M290, about 30 µm layers | page\* |
| 19 | Institute of Light Materials and Technologies (Rusal), probably RS-553 type | EP3903964B1, WO2020117090A1, RU2744075C2 (US2021/0291270 abandoned). [link](https://patents.google.com/patent/EP3903964B1/en) | 2018; EP granted 2023, lapsed in GB and some other states | Mg 4.5–6.5; Cr 0.35–0.80; Zr 0.40–1.0; B 0.002–0.12; Mn+Fe+Ni 0.05–0.8. Claim 2: Cr/Zr 0.5–1.5 | Annealed 400 °C/5 h (UTS/YS/El, HV): Al-4.5Mg-0.8Cr-0.8Zr-0.12B 420/310/14, 119. Al-5.2Mg-0.5Cr-1.0Zr-0.05B 440/340/12, 128. Al-6.5Mg-0.6Cr-0.4Zr-0.002B 420/330/13.5, 122 | Mg solid solution; supersaturated Cr; Al3Zr; borides | **Melt 810–850 °C, hold 1 h at 790–820 °C, superheat ≥100 °C above liquidus (claim 3)**, carnallite flux, B added as Al-5B, N2+O2 gas. EOS M290, 250 W | page\* |
| 20 | Rusal ETC, probably RS-300 type | RU2717441C1, EP3623488B1, US11802325B2, WO2019226063A1. [link](https://patents.google.com/patent/RU2717441C1/en) | 2018; granted | Mg 4.0–6.5; Zr 0.5–1.0; Sc 0.2–0.6; Ca 0.005–0.2; O 0.001–0.2 | Tables are images. Stated targets: UTS ≥470 MPa, El ≥11% after a 400 °C anneal | Al3(Sc,Zr); Al4Ca | **Melt 850–950 °C for the Sc/Zr additions, Mg added at ≤820 °C, superheat 160–250 °C**, N2 or Ar + 0.2–1% O2. 180 W, 30 µm, base plate of the same alloy | page\* (claims and process only) |
| 21 | Rusal ETC, probably RS-333 type | US12077837B2, RU2730821C1, EP4083244B1. [link](https://patents.google.com/patent/US12077837B2/en) | 2019; active | Ni 2.5–5.5; Mn 1.0–3.5; Fe 0.15–2.0; Zr 0.2–1.0; Ce 0.05–0.4; Cu+Zn 0.05–1.5; Si+Ca 0.1–2.0; Ni > Mn+Fe. As-printed UTS ≥370 | As printed, vertical (UTS/YS/El): Al-1.5Mn-3.9Ni-2.0Fe-0.8Zr-0.1Ce-0.5Si-0.5Ca 453/355/5.1. Al-3.5Mn-5.5Ni-0.15Fe-0.6Zr-0.28Ce 481/357/4.2. Ex. 3: 345/292 at 200 °C. Stable after 300 °C/3 h | Al16Mn3Ni / Al9FeNi eutectic plus Al3Zr | **Superheat ≥100 °C** (Ex. 3 used 80 °C). EOS M290, 280–320 W, 400–1200 mm/s, ≤45 µm | page\* |
| 22 | Institute of Light Materials and Technologies (Rusal) | US12209297B2, RU2741022C1. [link](https://patents.google.com/patent/US12209297B2/en) | 2019; granted 2025 | Cu 6.0–7.0; Mg 0.2–0.8; Mn 0.3–1.0; Ce 0.1–0.7; Si 2.8–3.7; Zr+Ti 0.45–0.9 | Quenched and aged, XY: Si 2.9 alloy 482/405 MPa/5.2%. Si 2.3–2.5 alloys cracked | Si eutectic backfill; Al8Cu4Ce | **Melt 870–920 °C, superheat ≥150 °C**. SLM 280HL, 250–350 W, **platform ≤160 °C** | page\* |
| 23 | Monash University; possibly Amaero "HOT Al" (not confirmed) | US11746396B2, US11976343B2, WO2019109135A1. [link](https://patents.google.com/patent/US11746396B2/en) | 2017; active | Mn 2.01–15; Sc 0.3–2.0; Mg 0–6; Zr 0–4 (rapid-solidified) | SLM **Al-4.52Mn-1.32Mg-0.79Sc-0.74Zr**: 427/453 MPa/12% as built; **577/588 MPa/11.3%** after 300 °C/5 h. Cast + laser remelt: Al-3Mn-1.5Mg-1Sc-0.05Zr 171 HV0.5; Al-4.18Mn-2Mg-0.9Sc-0.18Zr 186 HV0.5 | Mn solid solution (better per wt% than Mg), direct ageing of Al3(Sc,Zr), low Mg limits evaporation | EOS M290, 370 W, 1000 mm/s, 0.1 mm hatch, 30 µm, 6061 plate | page\* |
| 24 | Höganäs AB with Chalmers University of Technology | WO2022122670A1, EP4259363B1, US20240043965A1. [link](https://patents.google.com/patent/US20240043965A1/en) | 2020; EP granted, US pending | Mn 3–5.5; Zr 0.2–2; Cr 0.2–1.4; Mg 0–2; Fe+Si ≤0.7; O ≤0.7 | HV0.3: Al-4.75Mn-0.75Cr-0.70Zr and -1.25Zr about 103 as printed, peak about 130–140 near 650–680 K (text inconsistent). Comparatives: **Al-4.75Mn-0.75Cr (no Zr)** peak 115; Al-4.75Mn-1.25Zr peak 105–110 | Scheil cracking index <20 °C; Mn/Cr solid solution, then Al6(Mn,Cr), Al12(Mn,Cr), Al3Zr | EOS M100, 170 W, 1000 mm/s, 0.13 mm, 30 µm. N2 atomised, 20–53 µm, O 0.35–0.55% | page\* |
| 25 | Iowa State / UT-Battelle / LLNL / Eck (Al-Ce-Mn) | US11608546B2. [link](https://patents.google.com/patent/US11608546B2/en) | 2020; active | Ce 4–20; Mn 5–15; Fe, Mg, Zr 0–2 | Al-10Ce-7.7Mn: YS 268 MPa, 1.1% at RT. 70 MPa at 400 °C | Metastable Al20Mn2Ce primaries | SiC crucible, Ar cover, N2 atomised. Concept Laser M2 | page\* |
| 26 | Iowa State / UT-Battelle / LLNL (Al-Ce-Cu) | US12247272B2. [link](https://patents.google.com/patent/US12247272B2/en) | 2019; active | Ce 6–35; Cu 3–35; Mn >0.5–3; others ≤2–5 | Al-6Ce-9Cu(-1Zr-0.45Mn); strength in figures only | Nano intermetallic network | Concept Laser M2, 900 W, 30 µm, **80 °C preheat** | page\* |
| 27 | Iowa State / UT-Battelle (Al-Ce-Ni) | US11986904B2. [link](https://patents.google.com/patent/US11986904B2/en) | 2019; active | Ce >0–35; Ni >1–35; Mn >0–3 | Al-9Ce-4Ni, Al-10Ce-3Ni-1Mn; figures only | Al23Ni6Ce4, Al11Ce3, Al3Ni network | N2 atomised | page\* |
| 28 | UT-Battelle (ACMZ for AM) | US20210285076A1. [link](https://patents.google.com/patent/US20210285076A1/en) | 2020; **abandoned** | Cu 5–35; Mn 0.05–3; Zr 0.5–5; Fe 0–3; Si <1 | Al-8.6Cu-0.45Mn-0.9Zr as built: UTS ≥250, YS 200–300 MPa, ≥10% El, about 118 HV | Al3Zr equiaxed nucleation; in-situ θ′ | Concept Laser M2, N2, 370 W, 1.3 m/s, **200 °C preheat**. 250 W gave hot tearing | page\* |
| 29 | Iowa State / UT-Battelle / Eck (Al-Ce-Mg) | US11491546B2. [link](https://patents.google.com/patent/US11491546B2/en) | 2016; active | RE 4–60; Mg ≥5 (claim 16: Ce 10–16) | Laser remelt and cast data only | Al11Ce3 | — | page\* |
| 30 | Alcoa → Howmet (Al-Fe-V-Si-Cu) | US20160138400A1. [link](https://patents.google.com/patent/US20160138400A1/en) | 2014; US **abandoned** | Fe 3–12; V 0.1–3; Si 0.1–3; Cu 1–6 | Al-8.1Fe-1.5V-1.7Si-2.1Cu built on EOS M280, >99% dense. No tensile data | AlFeVSi dispersoids | Inert-gas atomised | page\* |
| 31 | Hamilton Sundstrand (RTX) | US11185923B2. [link](https://patents.google.com/patent/US11185923B2/en) | 2017; active | Ce >2–<4; Ti 0.5–2.5; Ni 0–3; N 0–0.75 | No property data | Ce particles plus Al-Ti-Ni intermetallics | Powder by melt, rapid solidification and grinding | page\* |
| 32 | Koiwai + Toyo Aluminium | US11555229B2, JP6393008B1, EP3616810. [link](https://patents.google.com/patent/US11555229B2/en) | 2017; active | Claim 1: Si 7–20; Mn 0.7–10; Cu 0.01–1.1; Fe ≤0.3; optional Mg 0.2–7, Ni 0.5–3. Claim 5: Si 4–30, Fe >0.3–2, Mn >1.5–10. Claim 6: Si 4–30, Fe 1–10, Mn ≤1.5, Cu 0.5–1.3. Claim 8: Si 4–30, Fe+Mn 2–10 with **plate >250–450 °C** | 200 °C plate, RT UTS: Al-Si base without Mn 290 MPa (410 on a 70 °C plate); +1.5Mn 550/3.5%; +5Mn 570/2.5%. **Al-7Mn (no Si or Mg) 330 MPa/7%, about 90 HV**. **Al-7Si-0.7Mg-0.7Mn 425–440 MPa**. 300 °C: AC8A+5Mn+3Cr+0.5Zr 150 MPa/29% | Mn/Cr/Fe intermetallics keep strength on a hot plate and resist cracking and distortion | **Plate 150–250 °C preferred**; EB up to 450 °C. Powder 35 µm | page\* |
| 33 | Toyo Aluminium + Osaka Research Institute | EP4227029A1. [link](https://patents.google.com/patent/EP4227029A1/en) | 2020; **pending** | Claims not read. Description: 0.20–13 total of at least one of Fe, Mn, Cr, Ni, Zr; Fe <4.5; Si <1 | Example tables garbled. Stated minimums: UTS ≥130 MPa at 200 °C, El ≥9% at RT | Dilute TM for heat resistance | EOS M280, 400 W, **preheat 35 or 200 °C**, 30–150 J/mm³. N2 atomised | page\* (description only) |
| 34 | Honda Motor | US11634794B2. [link](https://patents.google.com/patent/US11634794B2/en) | 2021; active | Si 3–20; Fe 1–7; Mn 0.1–7 with α-AlFeSi | Al-6.8Si-0.5Fe-0.4Mg: El 6% → 12% with +0.5Mn. Al-10Si-1Fe: 2% → 4% with +1Mn | Mn converts β-AlFeSi to α | ≥10^4 °C/s; pulverised ingot | page\* |
| 35 | Honda Motor | JP7832831B2, US20230311211A1. [link](https://patents.google.com/patent/JP7832831B2/en) | 2022; granted 2026 | Ti 0.1–3; Si 3–20; Cu 0.1–10; Mg 0.1–3; Fe 0.05–5; Zr, Mn ≤3; Ni ≤5; Cr ≤1; Zn ≤3 | E ≥80 GPa, El ≥3%; tables not on the page | — | Gas atomised, 10^5 °C/s | page\* (claim wording has a rendering placeholder) |
| 36 | Central South University + CRRC | CN109487126B, WO2020125553A1. [link](https://patents.google.com/patent/CN109487126B/en) | 2018; active | Mg 3–9; Sc 0.3–0.8; Zr 0.1–0.6; Mn 0.1–1; Cu 0.2–2.5; Si 1–3; Zn 0.1–1.2 (some examples fall outside the claim) | SLM UTS/El: Al-9Mg-0.8Sc-0.55Zr 485/17% as built, 550/15% after 288 °C/4 h. Al-4.5Mg-0.6Sc-0.3Zr 463/24%, 505/22% after 325 °C/12 h. **Al-3.2Mg-0.36Sc** 453/26%, 502/25%. No YS | Al3(Sc,Zr) | **Ar atomisation, melt 780–900 °C**, 7–8.6 MPa. **Plate 180–300 °C**, 200–400 W, 30–50 µm | page\* |
| 37 | 3D Lab Sp. z o.o. (AMAZEMET group), ultrasonic atomisation | US12090554B2. [link](https://patents.google.com/patent/US12090554B2/en) | 2019; active (page flags family litigation) | Process: arc melts a pool directly on the sonotrode (no crucible), ultrasound 15–1000 kHz | Examples are Pt and CuNi3Si, not Al | — | **Pool at 1.0–1.3 × Tm (K)**; Ar 0.01–6 bar or vacuum; D50 25–65 µm | page\* |

Secondary leads checked only briefly by the sub-agent (page\*, few details):

- **CN109280820B** (Beijing Institute of Aeronautical Materials): Sc-free Al-7Si-7Zn-1.5Mg-1Cu-0.15Zr-0.1Ni, UTS >500 MPa. Atomised at 750–900 °C.
- **EP4012062A1** (Acts Technologies, withdrawn): Mg 7–25 with Sc+Zr 0.5–2. Al-7Mg-0.7(Sc+Zr) gave YS 400, UTS 500 MPa, 20% El.
- **CN117684056A** (Xi'an Bright Laser Technologies): Al-Zn-Mg-Cu with Sc 0.4–1.3.
- **US12540377B2** (Shanghai Jiao Tong University): Al-Ce-Mg-Y-Zr powder, atomisation data only.

**Not found** in the time available (searched once or twice, no number located; this does not mean no patent exists):

- Northwestern-assigned Al-Zr-Er/Sc/Yb/Si AM filings. A "NUAdd" alloy series is listed as patent pending, with no number given.
- Rusal Al-Ca and an RS-230 Al-Si-Mg-Cu patent.
- Elementum product-specific (A6061-RAM2 etc.) claims.
- Rheinfelden, Hydro, Trimet, Gränges and PEAK/Erbslöh AM patents.
- EOS Al2139 AM and Al5X1. EOS's datasheet gives Al5X1 as Mg 2.5–4.2, Zr 0.6–1.8, Mn 0.1–1.0; that is a datasheet, not a patent.
- Mercury Marine, Equispheres, 3D Systems, Daido, UACJ, Nippon Light Metal, Kobe Steel.
- BJUT Er-microalloyed CN patents (only journal papers found, e.g. SLM Al-Mg-Mn-Er-Zr with about 440 MPa YS, 520 MPa UTS, 15.5% El).
- UTC/Pratt Al-Cr-Mn-Co-Zr quasicrystal AM alloys.
- An aluminium-specific ultrasonic atomisation patent.

---

## A. White space (Al ≥85 wt%, 2–5 additions from Mn, Cr, Zr, Mg, Si, Cu, Ti, Fe, Ni, Ce, Sc, Li, Er, Zn, Sn)

These are observations from about 37 families read in one session, not a freedom-to-operate search. "Not found" means I did not find a claim, not that nobody has claimed it.

**Heavily claimed (avoid, or license):**

- **Al-Mg-Sc(-Zr)**: Airbus (Sc ≥0.6 in US11433489; any Al-Sc via AM in DE102007018123, expiring 2027), Rusal (+Ca), CSU.
- **Al-Mn-Sc**: Monash claims any Mn 2.01–15 with Sc 0.3–2, Mg 0–6, Zr 0–4. Any Mn-rich Sc-bearing composition sits inside it.
- **Al-Mg-Zr (Sc-free)**: NanoAL claims Mg 1–10, Zr 0.3–3 for AM.
- **Al-Mg-Cr-Zr(-B)**: Rusal.
- **Al-Mn-Cr-Zr (Mg 0–2)**: Höganäs.
- **Al-Mn-Ni-Cu-Zr**: Constellium (EP granted).
- **Al-Ni-Mn-Fe-Zr-Ce**: Rusal.
- **Al-Fe and Al-Fe-Zr**: Constellium. Fe 2–8 alone (Zr optional) in US12378641; Fe 0.5–2.5 + Zr 0.5–2.5; Fe 1–3.7 + Zr/Er/Sc/Ti.
- **Al-Si-Mn and Al-Si-Fe-Mn**: Koiwai/Toyo (Si ≥4 or ≥7 in every independent claim), Honda.
- **High-Mg Al-Mg-Ti-B-Be**: Fehrmann (Mg 9–14).
- **Al-Mg / Al-Mg-Si / Al-Zn-Mg with Fe 0.5–1.5 + Mn ≤0.9**: AMAG/Audi.
- **Al-Zn-Mg-Cu(-Zr)**: QuesTek, HRL.
- **Al-Ce-(Mn, Cu, Ni, Mg)**: ORNL/Ames, including Ce as low as >2 with Ti in Hamilton Sundstrand.
- **Dilute Al-(Fe, Mn, Cr, Ni, Zr) 0.2–13 total**: Toyo EP4227029 is **pending**, and I did not read its claims. If it grants broadly it could reach many dilute TM combinations, so watch it.

**Thin or not found (Sc-free, low or no Zr):**

1. **Al-Mn-Mg without Sc or Zr** (e.g. Al-(2–5)Mn-(1–4)Mg). Monash needs Sc; Höganäs needs Zr and Cr; AMAG caps Mn at 0.9 and needs Fe 0.5–1.5. I did not find a claim, apart from the possible reach of the pending Toyo EP4227029. Al-Mn-Mg-Er(-Zr) appears in BJUT journal papers, which are prior art rather than claims.
2. **Al-Mn-Cr without Zr, and Al-Mn-Cr-Mg/Ti.** Höganäs requires Zr ≥0.2, and its Zr-free Al-4.75Mn-0.75Cr is a *comparative* example there. Koiwai's Mn-Cr examples carry ≥4 Si. I did not find a claim for Si-free, Zr-free Al-Mn-Cr, but the pending Toyo EP4227029 again needs checking.
3. **Al-Mg-Er or Al-Mn-Er without Sc and Zr.** QuesTek's Er claim needs Zn 3–9 and Zr 0.5–2. Airbus DE'123 lists Er only as an optional addition to Sc. I did not find a claim.
4. **Al-Ni-Mn and Al-Ni-Cr (no Zr, Ce or Cu).** Rusal needs Zr + Ce + Cu/Zn + Si/Ca; Constellium needs Cu + Zr; ORNL needs Ce. Not found.
5. **Al-Fe-Mn-Mg with Fe >1.5 and Zr-free.** AMAG stops at Fe 1.5; Constellium's Fe claims cap Mg at ≤0.2–0.5. Not found except for the pending Toyo filing.
6. **Al-Cr-Mg(-Ti), Al-Mn-Ti, Al-Cr-Ti.** Not found as AM claims. Ti appears mainly as a grain refiner (Fehrmann Ti-B; Airbus Ti-Sc-Zr, abandoned).
7. **Sn- and Li-containing AM alloys.** I did not find claims; Li appears only as an optional element in long lists.

## B. Seed candidates from patent examples (makeable from Al, Si, Mg, Mn, Cr, Zn, Sn, Ti + small Sc/Er; Fe, Cu, Ni buyable; Zr uncertain)

| # | Composition (wt%) | Source | Reported properties | Notes |
|---|---|---|---|---|
| 1 | **Al-7Mn** | US11555229B2 (Koiwai/Toyo) | UTS 330 MPa, 7% El, about 90 HV, 200 °C plate | Binary, no Zr. Composition from page\*, so check the PDF |
| 2 | **Al-7Si-0.7Mg-0.7Mn** | US11555229B2 | UTS 425–440 MPa | Inside Koiwai claim 1 (FTO caution) |
| 3 | **Al-4.75Mn-0.75Cr** | US20240043965A1 / EP4259363B1 (Höganäs) | Peak about 115 HV0.3 after ageing (hardness only) | Comparative there, so outside Höganäs's claim (needs Zr ≥0.2) |
| 4 | **Al-3.2Mg-0.36Sc** | CN109487126B (CSU/CRRC) | UTS 453 MPa / 26% as built; 502 MPa / 25% after ageing | Zr-free, low Sc. Inside Airbus DE'123 (Al-Sc via AM; expires about 2027) |
| 5 | **Al-4Fe** | US12378641B2 (Constellium) | 282/405 MPa/4.5% as built; 262/378/7.4% after 400 °C/1 h; 200 °C plate | Binary, needs Fe. Claimed by Constellium |
| 6 | **Al-6.3Zn-3.2Mg-1.1Cu-0.1Zr** | US10941473B2 (QuesTek) | 183 HV in T7, crack-free (DMLS) | 0.1Zr is minor; may print without it but untested. Claimed |
| 7 | **Al-6.8Si-0.5Fe-0.4Mg-0.5Mn** | US11634794B2 (Honda) | El 12% (vs 6% without Mn) | Ductility data only |
| 8 | **Al-3Mn-1.5Mg-1Sc-0.05Zr** | US11746396B2 (Monash) | 171 HV0.5 after 300 °C/24 h (cast + laser remelt, not a full build) | Sc 1 wt% may exceed "small amounts". Claimed by Monash |
| 9 | **Al-10.9Mg-0.3Ti-0.005B(-0.015Be)** | US12281374B2 (Fehrmann) | Permanent mould, 400/202 MPa/25% after 450 °C/24 h (castings, not LPBF) | Be is toxic; dropping it leaves the claim but changes the alloy. Expect Mg loss in atomisation |
| 10 | **Al-1.78Zr-1.04Fe** or **Al-0.81Zr-1.83Fe** (only if Zr is obtained) | US12377463B2 (Constellium) | 298/307 MPa/7.8% (400 °C/1 h); 278/316/18.8% (400 °C/4 h) | Best-documented Zr route, with full LPBF settings |

If Zr is obtained, the next options are Al-4.52Mn-1.32Mg-0.79Sc-0.74Zr (Monash: 577/588 MPa/11.3%) and Al-5.2Mg-0.5Cr-1.0Zr-0.05B (Rusal: 440/340 MPa/12%). Both are claimed.

## C. Process hints found in the patents

**Melt temperature for Zr-bearing melts:**

- NanoAL (US11603583) melt-spun its Al-Mg-Zr at a **casting temperature above 1100 °C**.
- Rusal Al-Mg-Sc-Zr-Ca (RU2717441) melts at **850–950 °C for the Sc/Zr additions**, adds **Mg only at ≤820 °C** to limit loss, and atomises at a **superheat of 160–250 °C** above liquidus.
- Rusal Al-Mg-Cr-Zr-B (EP3903964) melts at **810–850 °C, holds 1 h at 790–820 °C, and claims superheat ≥100 °C**, with carnallite flux and B added as Al-5B master alloy.
- Rusal Al-Ni-Mn-Fe-Zr-Ce uses superheat ≥100 °C.
- Rusal Al-Cu-Si-Ce-Zr/Ti uses **870–920 °C, superheat ≥150 °C**.
- Airbus Al-Mg-Sc-Zr melts at **≥700 °C (≥800 °C preferred)**.
- CSU Al-Mg-Sc-Zr is atomised from a **780–900 °C** melt (Ar, 7–8.6 MPa); BIAM's Al-Zn-Mg-Si-Zr from 750–900 °C.

**Ti, Cr and Mn melts:**

- No patent gave a specific superheat for Cr- or Mn-bearing melts.
- Rusal's Cr-Zr alloy used the 810–850 °C window above.
- Fehrmann's Ti-B high-Mg alloy melts at only **650–800 °C**.
- Ames used a **SiC crucible under Ar cover** for Al-Ce-Mn.
- The 3D Lab ultrasonic patent holds the pool at **1.0–1.3 × Tm in kelvin** on the sonotrode with no crucible, which for Al works out to up to about 940 °C.

**Mg loss:** Constellium states that Mg evaporates during atomisation and SLM. Monash prefers low Mg partly for that reason. Rusal adds Mg last at a lower temperature.

**Atomising gas:** Several Rusal patents deliberately use **N2 or Ar with 0.2–1% O2**, apparently to passivate the powder.

**Build-plate heating:**

- Constellium used **200 °C** throughout (25–150 °C reported processable; 50–300 °C beneficial).
- Koiwai: **150–250 °C preferred**. Its Mn-free Al-Si reference dropped from 410 to 290 MPa on a 200 °C plate, while the Mn-bearing alloys kept 550–575 MPa. Up to 450 °C for electron beam.
- ORNL ACMZ: **200 °C** (and 370 W rather than 250 W) avoided hot tearing.
- ORNL Al-Ce-Cu: 80 °C.
- CSU: 180–300 °C.
- Rusal Al-Cu-Si-Ce: ≤160 °C.
- Toyo: 35 or 200 °C.
- Constellium HT1: 100–200 °C.

**Post-build heat treatment:** Typical schedules are stress relief at 300 °C for 2–4 h, then direct ageing at 300–425 °C:

- Al3(Sc,Zr) peaks around 300–325 °C.
- Al3Zr-only alloys peak around 400–425 °C (NanoAL, Constellium).
- Höganäs Al-Mn-Cr-Zr peaks near 375–405 °C.

## D. Freedom-to-operate caution

This is a short, single-session literature survey made from Google Patents pages and search results. It is not legal advice and not a freedom-to-operate opinion. Status and expiry dates are Google's estimates. Claims were often read in truncated form, and the sub-agent-read entries (page\*) were not re-checked by me. Patent rights vary by country, and continuations, divisionals and pending applications (e.g. Toyo EP4227029, Höganäs US20240043965) can change scope. Many families were not searched at all (see "Not found"). Academic research use may still be infringing in some jurisdictions, and any move toward publishing compositions for commercial use, licensing powder, or making parts for partners should go through the university's technology-transfer or legal office, with a professional search against the specific compositions chosen.
