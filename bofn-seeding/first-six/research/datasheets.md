# Commercial LPBF aluminium alloys: vendor datasheets, process statements, Aconity MIDI and AMAZEMET rePOWDER

Compiled 2026-11-26 from direct downloads of vendor pages and PDFs (text extracted with pypdf). The
source column gives the URL actually read. `datasheet` = value read in the vendor's own PDF or page
(including a machine OEM's datasheet for that powder); `secondary` = trade article, reseller,
distributor, conference abstract or paper; `unverified` = only a search-engine summary. Orientation
pairs are written V/H (vertical / horizontal) unless stated. YS = 0.2 % yield, UTS = tensile strength,
El = elongation at break. AB = as built, SR = stress relieved, DA = direct aged, HT = heat treated.

Blocked or unreadable: metal-am.com (HTTP 403 to both fetch routes), mdpi.com (403), rusalofamerica.com
(no connection), aconity3d.com "LAB" page (empty), Velo3D PDFs (redirect to HTML), several search
calls refused by the search tool itself (AMAZEMET product page via WebFetch, one 3D Lab ATO query);
those pages were then read with curl instead where possible.

---

## Table 1: Commercial LPBF aluminium alloys

### 1a. Sc-free alloys

| Vendor | Product | Composition (wt%) | Powder cut / atomization | Machine / parameters | Heat treatment(s) | YS / UTS / El by condition | Hardness | Other | Critical minerals | Source | Verified? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ECKART (ALTANA; ex-AMT/Aeromet) | A20X powder (sold as "A205 gas atomised powder", AMS 4471) | Al bal; Cu 4.2-5.0; Mg 0.20-0.33; Ag 0.6-0.9; Ti 3.00-3.85; B 1.25-1.55 (TiB2); Si ≤0.1; Fe ≤0.08; others ≤0.08 each | D10 20 µm / D90 63 µm, gas atomised | "compatible with all leading LPBF" machines; no layer/plate stated | SR 300 °C 2 h on plate; proprietary T7 (solution, quench, age) | AB: 350-385 / 357-394 / 12-15 %. SR: 310 / 312 / 20 %. T7: 390-440 / 450-511 / 10-13 %. 200 °C (T7): 311 / 331 / 15 % | ≥140 HV | >99.7 % density without HIP; "double the strength of an Al-Sc alloy at 200 °C" | Ag 0.6-0.9; Ti/B (TiB2) | https://www.eckart.net/download/document/view/id/216/ (datasheet, Sept 2020); https://www.eckart.net/en/markets-overview/eckart-am/a20x | datasheet |
| Höganäs | forAM Al-HS1 20-63 GA (Chalmers-derived Al-Mn-Cr-Zr) | Al bal; Mn 4.8; Cr 0.8; Zr 0.8 (typical) | 20-63 µm (max 5 % over/under), gas atomised; Carney flow 15 s/50 g; AD 1.40, TD 1.76 g/cm³; 10 kg drums under Ar | not stated | DA 375 °C in air, 4 h or 6 h | Z: AB 220 / 280 / 25 %; DA 4 h 355 / 420 / 16 %; DA 6 h 350 / 430 / 13 %. XY: AB 220 / 285 / 25 %; DA 4 h 370 / 440 / 12 %; DA 6 h 365 / 445 / 11 % | not stated | Anodizable (Type II, no corrosion after 336 h ASTM B117); better corrosion than AlSi10Mg | Zr 0.8; Cr 0.8 | https://www.hoganas.com/globalassets/downloads/libary/additive-manufacturing_foram-al-hs1-20-63-ga_3312hog.pdf | datasheet |
| Höganäs | forAM Al-HS2 | not published | 20-63 GA | - | DA | ">400 MPa" strength at RT after DA (type of strength not stated); HS1 keeps ~200 MPa at 250 °C | - | - | not stated | https://pr.mono.ipros.com/en/hoganas/product/detail/2001560745/ (Höganäs Japan listing on a catalogue platform) | secondary |
| EOS (now "EOS Aluminium Constellium Al5X1", July 2026) | Al5X1 (AA 5A05.50) | Al bal; Mg 2.5-4.2; Zr 0.6-1.8; Mn 0.1-1.0; Fe ≤1; Si ≤1; Ti ≤1 | 20-63 µm | EOS M 290, 40 µm, argon, EOS grid nozzle, HSS blade, sieve 75 µm (plate temperature not given); also M 400-4, 40 µm | DA 6 h at 400 °C, gas quench, inert preferred | ASTM E8: AB 240/260 / 310 / 23 %; DA 380/385 / 415 / 14.5 %. ISO 6892: AB 230/255 / 310 / 23 %; DA 380 / 410 / 13-13.5 % | AB 86 HBW (40 HRB); DA 127 HBW (71 HRB) | 132 W/m·K (DA); anodized MIL-A-8625 Type III | Zr up to 1.8 | https://www.eos.info/metal-solutions/metal-materials/data-sheets/mds-eos-aluminium-al5x1 ; https://www.eos.info/metal-solutions/data-sheets/aluminium/pds-eos-aluminium-al5x1-eos-m-290-40um ; rename: https://www.eos.info/press-media/press-center/press-releases/2026/strategic-partnership-with-constellium | datasheet |
| Constellium (also EOS, 3D Systems, Nikon SLM, Velo3D, AddUp, Eplus3D) | Aheadd CP1 (AA8A61.50, SAE AMS 7074) | Al bal; Fe 0.8-1.4; Zr 0.9-1.4 (3D Systems, Nikon SLM). EOS spec: Fe 0.8-1.2; Zr 0.9-1.35; Si ≤0.3 | 20-63 µm (EOS, Nikon SLM) | EOS M 290, 60 µm, **plate 125 °C**, grid nozzle; 3D Systems DMP Flex 350 Triple 60 µm; Nikon SLM 500 90 µm, NXG 600 60 µm | single step, no quench: 4 h at 400 °C ("HT1" in Nikon SLM's sheet; "SR" in 3D Systems') | EOS 60 µm: AB 140/150 / 200 / 18/19 %; HT 300 / 340 / 10/12 %. 3D Systems: NHT 130 / 190 / 30 %; 400 °C 4 h 290 / 330 / 20 %. Nikon SLM 500 (90 µm, machined, mean): NHT 120 H, 115 V / 185, 180 / 24, 23 %; HT1 275 / 305, 300 / 16, 14 %. NXG 600: HT1 V 295 / 315 / 16 % | EOS 55 → 95 HBW; Nikon 56 → 98 HV5 | Conductivity 28 → 46 %IACS (EOS); 18 → 28 MS/m (3DS); "thermal stability up to 300 °C"; Type II/III anodizable; walls to 0.3 mm | Zr ~1 | https://www.eos.info/metal-solutions/data-sheets/aluminium/pds-eos-aluminium-constellium-cp1-eos-m-290-60um ; https://de.3dsystems.com/sites/default/files/2023-12/3d-systems-aheadd-cp1a-mds-letter-us-reva-web.pdf ; https://nikon-slm-solutions.com/wp-content/uploads/2024/07/mds5144.pdf | datasheet |
| Constellium | Aheadd HT1 | "Al-Mn-Ni-Cu-Zr system" (no ranges) | not found | not found | not found | not found; "thermally stable for service temperatures up to around 300 °C" | - | aimed at replacing Ti in some parts | Zr, Ni | Constellium-authored conference abstract: https://airdrive.eventsair.com/eventsairwesteuprod/production-atpi-public/cb7c330559f64e55bf3c1e6ce912741b ; Constellium powder page (https://constellium.com/products/aluminium-powders) now shows no grade data | secondary |
| EOS | Al2139 AM (modified from AA 2139) | Al bal; Cu 4.5-5.5; Mg 0-0.8; Ag 0.15-0.6; Mn 0.2-0.6; Zn ≤0.25; Si ≤0.1; Fe ≤0.15; Cr ≤0.05; V ≤0.05 (one further row on the page had no element label) | 20-63 µm | M 290, 60 µm, **plate 175 °C**, Ar, sieve 75 µm; M 400-4, 50 µm, **plate 195 °C** | Solution 45 min 490 °C, water quench, natural age 3 days (T4) | AB 350 / 380 / 6 V, 8 H %; HT 460 / 520 V, 540 H / 4 V, 6 H % | AB 112, HT 162 HBW | "outstanding performance up to 200 °C" | Ag 0.15-0.6 | https://www.eos.info/metal-solutions/metal-materials/data-sheets/mds-eos-aluminium-al2139-am ; https://www.eos.info/metal-solutions/data-sheets/aluminium/pds-eos-aluminium-al2139-am-eos-m-290-60um | datasheet |
| EOS | AlF357 (AlSi7Mg0.6) | composition table not shown on the page read | not shown | M 290, 30 µm, **nitrogen**, sieve 106 µm (plate temperature not given); M 400, 60 µm, N2 | T6-like: 540 °C 30 min, water quench; 165 °C 6 h | AB 250/255 / 400/365 / 6/10 %; T6 265/270 / 330/340 / 11.5 % | - | 140 (AB) / 150 (T6) W/m·K | none | https://www.eos.info/metal-solutions/data-sheets/aluminium/pds-eos-aluminium-alf357-eos-m-290-30um | datasheet |
| EOS | AlSi10Mg (EN AC-43000, ASTM F3318) | Al bal; Si 9-11; Mg 0.2-0.45; Fe ≤0.55; Mn ≤0.45; Ti ≤0.15; Zn ≤0.1; Cu, Ni, Sn ≤0.05; Pb ≤0.03 | 25-70 µm | M 290: 30 µm **plate 35 °C**; 60 µm **100 °C**; 1 kW 80 µm **125 °C**; Ar, sieve 90 µm | SR 270 °C 90 min; T6 530 °C 30 min WQ + 165 °C 6 h | 30 µm: AB 233/270 / 466/461 / 6.3/10.2 %; T6 250/260 / 310/320 / 11 %; SR 200 / 310 / 9 % | AB 114, T6 105 HBW | fatigue 110 MPa (AB, 2×10⁷) | none | https://www.eos.info/metal-solutions/metal-materials/data-sheets/mds-eos-aluminium-alsi10mg ; https://www.eos.info/metal-solutions/data-sheets/aluminium/pds-eos-aluminium-alsi10mg-eos-m-290-30um | datasheet |
| Elementum 3D | A5083-RAM2 | A5083 (Al-4.5Mg-0.15Cr-0.7Mn) + 2 % RAM additives (ceramic, identity not disclosed) | not stated | EOS M290, 40 µm parameters | none required | AB 359 / 421 / 15 % | 62.7 HRB | E 74.7 GPa; 7.2 mm³/s | not disclosed | https://www.elementum3d.com/wp-content/uploads/2025/05/MKT-EXT-00471-A5083-RAM2-Web-Data-Sheet-2025-05-05.pdf | datasheet |
| Elementum 3D | A5083-RAM5 | proprietary A5083 + 5 vol % ceramic | not stated | EOS M290, 40 µm | none; optional SR 300 °C 2 h | AB 407 / 462 / 9.8 %; SR 421 / 476 / 10 % | - | E 81.7 GPa | not disclosed | https://www.elementum3d.com/wp-content/uploads/2024/10/MKT-EXT-00472-A5083-RAM5-Web-Data-Sheet.pdf | datasheet |
| Elementum 3D (also 3D Systems "Certified A6061-RAM2 (A)") | A6061-RAM2 | A6061 (Al-1.0Mg-0.6Si-0.28Cu-0.2Cr) + 2 % RAM | not stated | EOS M290, 40 µm (A6061-RAM2_40um_M290_v0.70); 3DS DMP Flex 350, 30 µm | T6 required (E3D-T6); 3DS "modified T6" | E3D T6: 297 / 331 / 12 %. 3D Systems (LT30, XY): 260 / 295 / plastic El not legible in extract | 60 HRB | 162 W/m·K; CTE 22.4 ppm/°C; anodizable (3DS); 250 °C YS 120 MPa | not disclosed | https://www.elementum3d.com/wp-content/uploads/2025/12/A6061-RAM2-2-pg-Web-Event-Data-Sheets-2025-12-18.pdf ; https://www.3dsystems.com/sites/default/files/2023-12/3d-systems-certified-a6061-ram2a-mds-letter-us-revc-web.pdf | datasheet |
| Elementum 3D | A2024-RAM2 | proprietary A2024 + 2 % ceramic | not stated | EOS M290 | E3D-T6 | 384 / 497 / 10 % | 80 HRB | 94 W/m·K (laser flash, stated as underestimate) | not disclosed | https://www.elementum3d.com/wp-content/uploads/2025/10/A2024-RAM2-Data-Sheet-2025-10-21.pdf | datasheet |
| Elementum 3D | A7050-RAM2 | A7050 (Al-2.3Cu-2.3Mg-6.2Zn) + 2 % RAM | not stated | EOS M290 | HIP + T74, or HIP + T6 | HIP+T74: 469 / 504 / 6.0 %; HIP+T6: UTS 586, YS printed as "80 ksi / 504 MPa" (internally inconsistent, 80 ksi = 552 MPa), El 3.5 % | 88 HRB (T74) | no SCC after 40 d at 62 ksi | not disclosed | https://www.elementum3d.com/wp-content/uploads/2024/10/MKT-EXT-00468-A7050-RAM2-Web-Data-Sheet.pdf | datasheet |
| Elementum 3D | A1000-RAM10 | A1000 + 10 % RAM | not stated | EOS M290 | none required | 260 / 320 / 11 % | 45 HRB | E 95 GPa; 112 W/m·K; "high temperature performance" | not disclosed | https://www.elementum3d.com/wp-content/uploads/2025/12/A1000-RAM10-Web-Data-Sheets-2025-12-18.pdf | datasheet |
| HRL Laboratories | 7A77.60L (powder 7A77.50) | Al bal; Zn 4.5-6.1; Mg 1.8-2.9; Cu 1.1-2.1; Zr 0.5-2.8; Cr <0.1; trace <0.15 | D50 20-65 µm available | not stated | HIP + heat treatment (ranges depend on both) | HT: 490-585 / 520-615 / 6-14 % | - | - | Zr up to 2.8 | https://www.hrl.com/products-services/materials/_assets/7A77-data-sheet.pdf (2019) | datasheet |
| Fehrmann Materials | AlMgty (brochure shows "AlMgty90C Ho") | not published ("no exotic/rare alloying elements"). Fehrmann patent family WO 2019/129723 claims ~9-14 Mg with Ti, Be, B (not confirmed to be AlMgty) | not stated | LPBF partner roeders | "Ho" single step, no quench | 3D printing: 452 / 547 / 8.8 % (condition as "Ho" implied, orientation not stated) | - | anodizable; seawater resistant | none stated | https://images.nuernbergmesse.de/files/50efdbf2-b670-e280-e56f-fce81d4cff5f.pdf (EN brochure); patent: https://brevets-patents.ic.gc.ca/opic-cipo/cpd/eng/patent/3086933/summary.html | datasheet (properties), unverified (composition) |
| Gränges Powder Metallurgy | Dispal S220 AM | AlSi35 | not stated | Concept Laser M2 (2021 rev.) | SR 4 h 500 °C | min: 115 / 200 / 1.5 % | - | E 90 GPa; CTE 15.1 ppm/K; 27 %IACS | none | https://granges.com/globalassets/09.-kampanjer/04.-granges-powder-metallurgy/03.-portfolio/granges_s220-am.pdf | datasheet |
| Gränges | Dispal S260 AM | AlSi25Cu4Mg1 | not stated | LPBF | SR; T66 | min: SR 150 / 250 / 2.1 %; T66 391.7 / 436.5 / 0.5 % | 167 HV30 | wear parts | none | https://prod.granges.com/globalassets/09.-kampanjer/04.-granges-powder-metallurgy/03.-portfolio/granges_s260-am.pdf | datasheet |
| Gränges | Dispal S250 | AlSi20Fe5Ni2 | powder offered | overview does **not** mark S250 as 3D-printed | - | not found | - | - | Ni | https://granges.com/contentassets/4931f1a18787412b848327d26ec5334e/240606-gpm_dispal_overview.pdf | datasheet (no S250 AM sheet found) |
| Gränges | GPM AlSi10Mg | Si 9-11; Mg 0.25-0.45; Fe ≤0.55; Mn ≤0.45 etc. | D10 26-32 / D50 40-45 / D90 53-61 µm, gas atomised | 50 µm layer | SR | AB 241 / 447 / 5 %; SR 184 / 285 / 12 % | - | - | none | https://granges.com/contentassets/4931f1a18787412b848327d26ec5334e/240606-gpm-alsi10mg.pdf | datasheet |
| Renishaw | AlSi10Mg-0403 | Si 9-11; Mg 0.25-0.45; Fe <0.25; O <0.20; N <0.20 etc. | 20-63 µm recommended (search excerpt of a Renishaw sheet; not in the 2015 sheet read) | AM250, 25 µm, 400 W | SR 300 °C 2 h | AB XY 264 / 442 / 9 %, Z 206 / 417 / 6 %; SR XY 211 / 334 / 9 %, Z 174 / 339 / 4 % | AB 119-123 HV0.5 | - | none | https://www.renishaw.com/media/pdf/en/0c48b4800c17480393f17ceaacb4ecdb.pdf | datasheet |
| RUSAL / IL&T | RS-300, RS-330, RS-356, RS-230, RS-390, RS-320, RS-333 | RS-300 = AlSi10Mg; RS-330 = AlSi9Cu3; RS-356 = AlSi7Mg; RS-230 = Al-Cu (to 250 °C); RS-390 = Al-Si-Ni (to 250 °C); RS-320 = Al-Si-Cu (unverified); RS-333 ≈ Al-3Si-0.5Mg (unverified) | not stated | RUSAL develops on EOS M290 400 W | - | not found on vendor pages | - | - | Ni (RS-390) | https://www.tctmagazine.com/rusal-america-additive-manufacturing-metal-powder/ ; https://www.rusal.ru/en/innovation/technology/additive (no compositions given) | secondary |
| NanoAL | Addalloy 3T, 5T, 7S, HX | 3T "Al-Mn-based", 250 °C; 5T "Al-Mg-based", heat-treatable; 7S "7000-series based"; HX "low-alloyed"; numbers not published | pre-alloyed, spherical | "across leading LPBF platforms" | simple thermal treatment | not published (datasheet behind request form) | - | HX for heat exchangers | not disclosed (patent family is Al-Mg-Zr/Er/Sc type, not verified) | https://nanoal.com/additive ; https://www.nanoal.com/addalloy-5t-powder ; https://www.invo.northwestern.edu/innovates/projects/addalloy-3t-5t-powders.html | datasheet (no numbers). "Unity Aluminum" link not found |
| BLT (Bright Laser Technologies) | BLT-AlAM500 | not disclosed | not stated | BLT machines | HT | HT: 480-500 / 530-550 / 11-17 % | - | aerospace | unknown | https://news.metal.com/newscontent/102867547/blt-alam500-the-cutting-edge-aluminium-alloy-designed-for-aerospace-3d-printing | secondary. "Al250C" not found |
| AM 4 AM | HiperAL | "zirconium derivative of a 7000-series powder", cold-plasma treated | - | - | - | YS 525 / UTS 550 (El not stated) | - | - | Zr | https://www.additivemanufacturing.media/products/am-4-ams-hiperal-aluminum-alloy-offers-enhanced-mechanical-properties-for-lightweight-applications | secondary |
| ORNL (alloyed by Eck Industries) | DuAlumin-3D | Al-9Ce-4Ni-0.5Mn-1Zr | atomised by Connecticut Engineering Associates; no commercial powder listing found | - | ~8 h HT | not found; >300 °C use | - | pistons, HCF +50 % vs cast | Ce (rare earth), Ni, Zr | https://3dprint.com/320336/ornl-continues-with-dualumin-3d/ | secondary |
| Amaero | HOT Al (Monash origin) | Al-Sc-Mn, age-hardenable; numbers not published | - | - | age hardening | not found; ~260 °C claimed | - | - | Sc | search summaries only; HOT Al not on current amaero.com.au site | unverified |
| Equispheres | NExP-1 AlSi10Mg (non-explosible) | AlSi10Mg | ">100 µm" average, spherical; designed for 700 W | 400 W trial in a university paper | - | not found in vendor doc | - | ASTM E1226 / JIS Z 8817 lowest explosion class | none | https://utw10945.utweb.utexas.edu/sites/default/files/2024/58%20Towards%20Affordable%20Aluminum%20Additive%20Manufactur.pdf | secondary |
| Valimet | AM Al powders | stocks AlSi10Mg, F357, 2024, 2219, 5083, 6061, 7075 "in tonnage"; custom atomization and sizing | size cuts not published | - | - | - | - | - | - | listing quoted in search (matmatch supplier page); valimet.com AM page lists only literature | secondary. A205/Scalmalloy from Valimet not found |
| Kymera / ECKA; EDAG / Rheinfelden | AM205; CustAlloy | CustAlloy: composition not published (CustoMat_3D project; powder by Kymera and Leibniz IWT; "wide property range from one alloy via heat treatment") | - | - | - | not found | - | - | - | https://www.edag.com/en/edag-group/newsroom/detail/new-crash-proof-aluminium-alloy-developed-for-3d-printing | secondary. AM205 not found |
| Mercury Marine | Mercalloy A362 | ~11 Si (HPDC casting alloy) | no AM powder found | - | - | - | - | - | - | search summary of Metals 2021, 11, 517 | unverified (not an AM powder in sources found) |
| AMAG | CrossAlloy .57 | composition not given; studied in LPBF at Chalmers (with 0.9 Fe blended) | inert-gas atomised | research | - | not found | - | - | - | https://research.chalmers.se/publication/553692/file/553692_Fulltext.pdf (search summary) | unverified |

### 1b. Sc-bearing alloys (for comparison)

| Vendor | Product | Composition (wt%) | Powder | Machine / parameters | HT | YS / UTS / El | Other | Source | Verified? |
|---|---|---|---|---|---|---|---|---|---|
| APWORKS (powder via Toyal and licensed producers) | Scalmalloy | Nikon SLM sheet: Mg 4.50-4.90; Sc 0.68-0.84; Mn 0.2-0.7; Zr 0.2-0.4; Fe ≤0.2; Si ≤0.2; Ti ≤0.15; O ≤0.05. Toyal: AlMg4.5Sc0.7Zr0.3 | 20-63 µm (Nikon SLM, Colibrium); Toyal ref. SCALMA40B5 | 3DS DMP Flex/Factory 350 30 and 60 µm; Colibrium M2 Series 5, 400 W, 50 µm, nitrogen, rubber recoater; Nikon SLM 280, 30 µm | 325 °C 4 h (APWORKS-advised) | APWORKS page: 480 / 520 / 13 %. 3DS SR: LT30 490 / 520 / 15.8 %; LT60 500 XY, 490 Z / 530, 520 / 14.0, 13.1 %. Colibrium: AB 295, 275 / 355, 350 / 23, 22 %; DA 475, 465 / 515, 505 / 12, 11.5 % | 95-100 W/m·K (3DS); Toyal: fatigue limit >160 MPa, stable to 250 °C; anodizable | https://www.apworks.de/scalmalloy ; https://3dsystems.com/sites/default/files/2022-02/3d-systems-certified-scalmalloy(a)-datasheet-usen-2022-02-23-a-print.pdf ; https://www.colibriumadditive.com/sites/default/files/M2SERIES5_Al-Mg-Sc_400W_CMDS_20250821_RevB%20%281%29.pdf ; https://www.indus3design.com/wp-content/uploads/2026/08/i3d-datasheets-nikon-slm-solutions-scalmalloy.pdf ; https://toyal-europe.com/wp-content/uploads/2022/09/Toyal-Scalmalloy.pdf | datasheet |
| APWORKS | Scalmalloy CX / HX / EX | not published (cryogenic / high-temperature / high-conductivity variants) | - | - | - | - | - | https://apworks.de/scalmalloycx (and /scalmalloyhx, /scalmalloyex) | datasheet (no numbers) |
| m4p | StrengthAl | Al-5.2Mg-0.8Zr-0.3Sc (Polimi paper with m4p); another source gives Mg 5.1, Sc 0.4, Zr 0.7 | - | EOS M290, 30 µm (m4p deck, not read: link 404) | 350 °C 6 h | not found | anodizable | search summaries only | unverified |
| RUSAL | RS-553 | Al-Mg-Sc, ~0.3 Sc per a 2025 paper | 20-45 µm used in that paper | - | - | not found | "lower cost than other Al-Sc AM alloys" | https://www.tctmagazine.com/rusal-america-additive-manufacturing-metal-powder/ | secondary |
| AMAZEMET Book of Powders | Al-4Cu-0.6Sc (No. 8) | as named | ultrasonic, 40 kHz, induction 850 °C | - | - | - | R&D powder, not a product line | https://configurator.amazemet.com/en/powders/08-al-4cu-0-6sc | datasheet |

---

## Table 2: What vendors say about powder and process

| Source | Powder size accepted / sold | Layer thickness | Build-plate preheat | Gas / oxygen / drying / flow |
|---|---|---|---|---|
| EOS (AlSi10Mg PDS) | 25-70 µm generic; sieve 90 µm | 30 / 60 / 80 µm | **35 °C (30 µm), 100 °C (60 µm), 125 °C (1 kW, 80 µm)** | Argon |
| EOS (Al2139 AM) | 20-63 µm; sieve 75 µm | 60 µm (M290), 50 µm (M400-4) | **175 °C (M290), 195 °C (M400-4)** | Argon, grid nozzle |
| EOS (Constellium CP1) | 20-63 µm | 60 µm | **125 °C** | grid nozzle |
| EOS (Al5X1) | 20-63 µm; sieve 75 µm | 40 µm | not stated | Argon, grid nozzle; inert furnace atmosphere preferred for DA |
| EOS (AlF357) | sieve 106 µm | 30 / 60 µm | not stated | **Nitrogen** |
| Nikon SLM (CP1, Scalmalloy, AlSi10Mg) | 20-63 µm for all three | 30 µm (Scalmalloy SLM 280), 60 µm (NXG CP1), 90 µm (SLM 500 CP1) | not stated in the sheets read | - |
| Colibrium (Scalmalloy) | 20-63 µm | 50 µm | not stated | Nitrogen; rubber recoater |
| 3D Systems (Scalmalloy, CP1, A6061-RAM2) | not stated | 30 and 60 µm | not stated | - |
| Elementum 3D | not stated | 40 µm parameter sets on EOS M290 | not stated | - |
| ECKART A20X/A205 | D10 20 / D90 63 µm "for all powder bed fusion machines" | - | - | reuse OK if oxygen and spatter controlled (vendor interview, https://3dadept.com/eckart-gmbh-on-the-use-of-high-strength-alloys-in-additive-manufacturing/) |
| HRL 7A77 | D50 20-65 µm options | - | - | - |
| Höganäs forAM Al-HS1 / AlSi10Mg | 20-63 µm, max 5 % over/undersize; Carney 15 s/50 g (HS1) | - | - | shipped in 10 L PE drums filled with Ar |
| Gränges GPM AlSi10Mg | D10 26-32, D50 40-45, D90 53-61 µm; custom PSD on request | 50 µm data | - | TD 1.6, AD 1.3 g/cm³ |
| AP&C / Colibrium powders | 15-45, 15-53, 20-63 µm "for different machines/build parameters" | - | - | stresses flow, fines and oxygen from surface area (https://go.additive.ge.com/rs/706-JIU-273/images/AP%26C_Aluminum_White%20paper_v1.pdf) |
| Equispheres NExP-1 | ">100 µm" average, for high layer thickness at 700 W | high | - | non-explosible class |
| Renishaw AlSi10Mg | 20-63 µm recommended (search excerpt) | 25 µm | - | O, N each <0.20 % in powder spec |
| Aconity (AconitySIEVE, from a Utah page) | - | - | - | sieve throughput 100-150 kg/h Al; residual O2 <500 ppm in sieve |

No vendor document read gave an explicit powder-drying procedure or a numerical oxygen limit for the build chamber for aluminium (the Aconity machine spec of <100 ppm is in Table 3).

---

## Table 3: Printer and atomizer

### 3a. Aconity3D machines (aconity3d.com product pages, read 2026-11-26)

| Item | AconityMIDI | AconityMIDI+ | AconityMINI |
|---|---|---|---|
| Build space | Ø170 × 200 mm; reductions Ø100 × 200 and Ø55 × 200 mm | Ø250 × 250; reductions Ø170, Ø100, Ø55 × 250 mm | Ø140 × 190; reductions Ø100, Ø55 × 190 mm |
| Lasers | up to 2, single- or multi-mode: 400 / 500 / 1000 / 1200 AFX / 1500 AFX / 3000 / 4000 W; green single-mode 200 or 400 W | up to 4, 200-4000 W, "multiple beam profiles", "different wavelengths available" | 1 laser, same power list as MIDI incl. green 200/400 W |
| Optics / spot | F-theta 80 µm; 3D scanning 80-500 µm | 3D scanning 80-500 µm | F-theta 80 µm; 3D scanning 80-500 µm |
| Preheat (max T / heated volume) | **500 °C / Ø170 × 180; 800 °C / Ø100 × 180; 1200 °C / Ø70 × 150 mm** | 500 °C / Ø250 × 180; 1000 °C / Ø150 × 150 mm | 500 °C / Ø140 × 150; 800 °C / Ø100 × 150 mm |
| Layer thickness | min 10 µm | min 10 µm | min 10 µm |
| Scan speed | max 12 m/s | 12 m/s | 12 m/s |
| Gas | Ar 4.6 or N2 at 6 bar, or vacuum <2 mbar; <5 L/min in process, <60 L/min purging | Ar / N2 | Ar / N2 / vacuum |
| Residual O2 | **<100 ppm** | <100 ppm | <100 ppm |
| Monitoring | coaxial pyrometer; coaxial high-speed CMOS | same | same |
| Other | exchangeable process chamber with optional external preparation station; 1450 kg | bidirectional vibrating powder deposition | 850 kg |

- Wavelength: not stated on any Aconity page read (an Austrian facility page calls its 400 W and 1000 W lasers "Nd-YAG"; MIDI+ at Turku lists "IR fiber"). Not verified.
- Minimum powder needed for the reduced build volumes: **not found** on aconity3d.com or facility pages.
- The aconity3d.com LAB page returned no content.
- **University of Utah** (Merrill Engineering Building; installed summer 2023): "Aconity MIDI; Ø170 × 200 mm; laser power 400 W; number of lasers 2; min layer 10 µm; induction heater to pre-heat build platform up to 1200 °C; pyrometer" (https://aerospace.research.utah.edu/?p=67 ; https://cores.utah.edu/?p=1670 ; https://mep.utah.edu/?p=4443, which says open architecture and "any weldable metal including aluminum alloys"). The same Utah page lists an AconitySIEVE (100-150 kg/h for Al, residual O2 <500 ppm). Whether the 1200 °C module fits the full Ø170 plate: per Aconity's table, 1200 °C applies to the Ø70 × 150 mm volume only, and 500 °C to the full plate.
- CMU: MIDI with optional second process chamber, preheating "up to 1200 °C" (https://engineering.cmu.edu/mfi/facilities/equipment-details/aconity-midi.html). Turku: MIDI+ Ø250 × 250, 400 W, 80 µm F-theta (https://utu.fi/en/susfab/equipment/open_source_multi_material_metal_ceramic_3d_printer_aconity_midi).

### 3b. AMAZEMET rePOWDER (https://amazemet.com/products/repowder/ ; FAQ https://www.amazemet.com/faq/ ; configurator https://configurator.amazemet.com)

| Item | Vendor statement |
|---|---|
| Frequency vs size | **20 kHz → d50 80-100 µm (EBM, DED); 40 kHz → d50 45-60 µm (LPBF, sintering); 60 kHz → d50 35-45 µm (LPBF, binder jet, thermal spray)**, "depending on the atomized material". No aluminium-specific d50 published. |
| Usable fraction | "narrow PSD allows up to 80 % of the powder to be used for dedicated technology" |
| Powder quality | Hall flow 4-5 g/s; sphericity (aspect ratio) d50 > 0.90 |
| Heat sources | Induction (alloys up to ~1300 °C: Sn, Zn, Mg, Pb, **Al alloys**, Cu, Ag, Au); arc/plasma (TIG; FAQ: up to 3000 °C); laser melting (wire feed, 40 kHz, launched Formnext 2026; pitched for limiting evaporation in Al alloys). Combined range "200 °C to 3500 °C". |
| Crucibles | Configurator: "Hybrid" = standard + induction module "processed in a **graphite crucible**". FAQ: graphite or ceramic crucibles may need changing by alloy; Zr/Ti/Hf master alloys should first be arc-melted in a water-cooled Cu crucible, then diluted in the induction melt. |
| Presets | rePOWDER Standard (plasma module, 40 kHz sonotrode, TIG, chiller); Hybrid (+ induction, graphite crucible); laser version (40 kHz, wire feeder). |
| Sonotrode | different sonotrode designs/materials by alloy and frequency; >30 h continuous life with proper use; 20-30 min to change. **Sonotrode/plate materials not named.** |
| Batch / throughput | "a few grams up to several kg per day (wire or induction)"; FAQ: feedstock input "typically a few to a few hundred grams"; continuous wire 1.2-2.4 mm, bar feeders up to 2 m |
| Gas | ~10 L/min |
| Changeover | 2-4 h for a full material change incl. cleaning |
| Aluminium in the vendor's "Book of Powders" | No. 5 AW-6082 AlSi1MgMn: induction 800 °C, 40 kHz, cast ingots. No. 7 Al + 20 vol % SiC: induction 850 °C, 20 kHz. No. 8 Al-4Cu-0.6Sc: induction 850 °C, 40 kHz. No. 9 Al-2Sr: induction 1200 °C, 40 kHz. PSDs, yields and compositions not shown in the page HTML. |
| Aluminium publications listed by vendor | "Additively Manufacturable High-Strength Aluminum Alloys with Coarsening-Resistant Microstructures Achieved via Rapid Solidification" (listed on the AMAZEMET technology and publications pages; details not read). Vendor aluminium page offers "modifications of AlSi10Mg, Al-Mg-Sc and experimental Al alloys" from grams to kg. |
| Application notes | Application-note category currently shows precious-metal notes only; no aluminium application note found. |
| Facilities | Georgia Tech AMPF ("coming soon"; induction to 1300 °C); TU Darmstadt / RMU (Ti, Ni, Al alloys). |

### 3c. 3D Lab ATO Lab Plus (comparison)

Ultrasonic atomization with TIG melting; vacuum pump for low oxygen; reactive alloys incl. Ti and Al;
feeders: wire, single-rod, multi-rod, revolver-rod; "several hundred grams per hour" at **20-120 µm**
(distributor brochure, https://analytik.co.uk/wp-content/uploads/2024/12/ato-lab-laboratory-atomiser.pdf).
Frequency options, crucible/induction module and Al-specific PSD: **not found**. 3D Lab's own pages
(https://3d-lab.pl/ato-lab/) are in Polish with no numbers; "ATO One" not found; ATO Sparq (compact,
AI monitoring) and ATO Noble (precious metals) are newer models. `secondary`.

---

## Section 4: Blog and trade articles

1. EOS-Constellium partnership (July 2026): CP1 joins EOS; Al5X1 renamed "EOS Aluminium Constellium Al5X1" and joins Constellium's portfolio. https://www.eos.info/press-media/press-center/press-releases/2026/strategic-partnership-with-constellium
2. Constellium conference abstract: CP1 = Al-Zr-Fe, no Mg/Zn (volatiles avoided), no-quench HT; HT1 = Al-Mn-Ni-Cu-Zr, stable to ~300 °C. https://airdrive.eventsair.com/eventsairwesteuprod/production-atpi-public/cb7c330559f64e55bf3c1e6ce912741b
3. EOS Al5X1 launch coverage (Oct 2023): ~410 MPa, 14 % El, single-step HT, anodizable. https://www.tctmagazine.com/eos-launched-aluminum-al5x1-metal-3d-printing-material/
4. ECKART interview on A20X: TiB2 gives equiaxed grains and crack-free LPBF on any machine; powder reuse depends on oxygen and spatter control. https://3dadept.com/eckart-gmbh-on-the-use-of-high-strength-alloys-in-additive-manufacturing/
5. RUSAL America powder line: RS-330 AlSi9Cu3, RS-356 AlSi7Mg, RS-230 Al-Cu and RS-390 Al-Si-Ni to 250 °C, RS-553 Al-Mg-Sc. https://www.tctmagazine.com/rusal-america-additive-manufacturing-metal-powder/
6. ORNL DuAlumin-3D (Al-9Ce-4Ni-0.5Mn-1Zr): >300 °C use, pistons with 50 % higher HCF than cast; alloyed by Eck, atomized by a contract atomizer. https://3dprint.com/320336/ornl-continues-with-dualumin-3d/
7. EDAG CustAlloy (CustoMat_3D): one alloy whose strength/elongation is tuned by downstream HT; powder by Kymera and Leibniz IWT. https://www.edag.com/en/edag-group/newsroom/detail/new-crash-proof-aluminium-alloy-developed-for-3d-printing
8. BLT-AlAM500: HT UTS 530-550, YS 480-500, El 11-17 %, composition withheld. https://news.metal.com/newscontent/102867547/blt-alam500-the-cutting-edge-aluminium-alloy-designed-for-aerospace-3d-printing
9. AM 4 AM HiperAL: Zr-modified 7xxx powder, YS 525 / UTS 550. https://www.additivemanufacturing.media/products/am-4-ams-hiperal-aluminum-alloy-offers-enhanced-mechanical-properties-for-lightweight-applications
10. TII AMALLOY3D-HT: alloy screened by blending commercial powders in situ, then made pre-alloyed in house by **ultrasonic atomization** for small batches; targets 300 °C. https://tii.ae/node/3595
11. CityU Hong Kong (Nature Communications, 2026): rare-earth-free LPBF Al with ~14 vol % intermetallic nanophases from recycled-Al impurity elements; 582 MPa UTS as printed, 114 MPa at 400 °C. https://www.cityu.edu.hk/mne/news-publications-seminars/3d-printed-aluminum-alloy-delivers-exceptional-heat-resistance-and-strength-without-rare-earths
12. Equispheres NExP-1 study: >100 µm non-explosible AlSi10Mg designed for 700 W; at 400 W needs reworked parameters; standard Al AM powders are 20-70 µm. https://utw10945.utweb.utexas.edu/sites/default/files/2024/58%20Towards%20Affordable%20Aluminum%20Additive%20Manufactur.pdf
13. AP&C aluminium white paper: PSD options 15-45 / 15-53 / 20-63 µm and why PSD drives oxygen, flow and parameter sets. https://go.additive.ge.com/rs/706-JIU-273/images/AP%26C_Aluminum_White%20paper_v1.pdf
14. Northwestern INVO on Addalloy 3T/5T: Al-Mn (250 °C) and heat-treatable Al-Mg pre-alloyed powders from the Dunand/Seidman Al-Mg-Zr work. https://www.invo.northwestern.edu/innovates/projects/addalloy-3t-5t-powders.html
15. AMAZEMET laser ultrasonic atomizer (Formnext 2026): laser melting of wire to limit evaporation in volatile alloys incl. Al. https://www.amazemet.com/amazemet-new-laser-ultrasonic-atomizer-at-formnext-2026/ (title only read)

---

## Section 5: Takeaways

**Highest-yield Sc-free commercial alloys at ≥ 8 % elongation (vendor datasheets):**

As built (no HT):
- ECKART A20X/A205: YS 350-385, UTS 357-394, El 12-15 % (Al-4.6Cu-0.75Ag-0.25Mg + ~5 % TiB2).
- Elementum A5083-RAM5: 407 / 462 / 9.8 % (SR 300 °C: 421 / 476 / 10 %); A5083-RAM2: 359 / 421 / 15 %. Ceramic additive not disclosed.
- EOS Al2139 AM: 350 / 380 / 8 % H only (6 % V).
- Everything else as-built sits at 120-270 MPa (CP1, Al5X1, Al-HS1, AlSi10Mg, AlF357).

Heat treated:
- HRL 7A77.60L: 490-585 / 520-615 / 6-14 % (HIP + HT; the low end of El is <8 %).
- Fehrmann AlMgty (brochure): 452 / 547 / 8.8 %; composition unpublished.
- ECKART A20X T7: 390-440 / 450-511 / 10-13 %.
- Elementum A2024-RAM2 T6: 384 / 497 / 10 %.
- EOS Al5X1 DA 400 °C 6 h: 380-385 / 410-415 / 13-14.5 %, with a simple no-quench treatment.
- Höganäs Al-HS1 DA 375 °C 4 h: 355-370 / 420-440 / 12-16 %.
- Aheadd CP1 400 °C 4 h: 275-300 / 300-340 / 10-20 %.
- Not qualifying: EOS Al2139 (460 YS but 4-6 % El); Elementum A7050-RAM2 (469 YS at 6 %).

**Compositions makeable from Al, Si, Mg, Mn, Cr, Zn, Sn, Ti + small Sc/Er, with Fe/Cu/Ni easy and Zr uncertain:**
- Without Zr: AlSi10Mg, AlF357/AlSi7Mg (EOS, Rusal RS-356), RUSAL RS-330 (AlSi9Cu3), Dispal S220 (AlSi35), S260 (AlSi25Cu4Mg1) and the S250 chemistry (AlSi20Fe5Ni2). Also the A5083 base (Al-4.5Mg-0.7Mn-0.15Cr) and the A6061 base (Al-1Mg-0.6Si-0.28Cu-0.2Cr), but Elementum's printability depends on an undisclosed ceramic (RAM) addition, so plain 5083 or 6061 will crack. A 7050 base (Al-6.2Zn-2.3Mg-2.3Cu) has the same problem.
- Needs Zr: Al5X1 (Zr 0.6-1.8), Al-HS1 (Mn 4.8, Cr 0.8, Zr 0.8), CP1 (Fe ~1, Zr ~1), 7A77 (Zr 0.5-2.8) and Scalmalloy (Zr 0.2-0.4). In every Sc-free alloy here the grain refiner is Zr or TiB2. A Mn-Cr base with Ti or Er replacing Zr (an Al-HS1 analogue) is the obvious lab experiment, but no vendor sells one.
- Not makeable: A20X (needs Ag and TiB2), Al2139 (Ag) and DuAlumin-3D (Ce).

**Powder cut and plate temperature vendors actually use:**
- Powder cut: almost everyone sells and qualifies **20-63 µm** gas-atomised powder (EOS for all its new grades, Nikon SLM, Colibrium, Höganäs, ECKART, Renishaw). EOS AlSi10Mg is 25-70 µm, Gränges D50 is 40-45 µm, AP&C also offers 15-45 and 15-53 µm, and HRL offers D50 from 20 to 65 µm.
- Layers: 30-60 µm (40 µm for Elementum and Al5X1).
- Plate temperature (EOS M 290/M 400 sheets are the only OEM documents that state one): AlSi10Mg 35-125 °C (rising with layer thickness and laser power), CP1 125 °C, Al2139 175-195 °C.
- Not stated in any sheet read: Al5X1, AlF357, Scalmalloy, A20X, Elementum and Höganäs plate temperatures.
- The Aconity MIDI's 500 °C full-plate heater covers all of these.
- rePOWDER at 60 kHz (d50 35-45 µm) or 40 kHz (d50 45-60 µm) brackets the 20-63 µm cut. The vendor's Al examples all used 40 kHz with induction melting at 800-850 °C in graphite.

**Not verified:** compositions for Addalloy, AlMgty, Aheadd HT1, HOT Al, CustAlloy, BLT and Chinese "high-strength" Al (no Sc-free Chinese grade with published chemistry was found); m4p StrengthAl and RUSAL numbers; Valimet size cuts; Kymera AM205; Mercury A362 as an AM powder; Aconity laser wavelength and minimum powder for reduced volumes; rePOWDER sonotrode materials, crucible maximum temperature and Al-specific PSD/yield; ATO frequencies.
