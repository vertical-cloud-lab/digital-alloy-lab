# Live reads, 2026-11-28 (round 3)

Every read is a row in [`live-reads-2026-11-28.csv`](live-reads-2026-11-28.csv), with its URL and UTC time.

**How.** Headed Chrome on a virtual display on the runner, its traffic sent through the lab's CubXL Pi over an SSH
SOCKS tunnel (it exits on BYU's network), driven with Playwright over CDP. Archived files came from the Wayback
Machine. Digi-Key's Cloudflare check cleared by itself when Playwright was detached for about 10 s while the page
loaded; no click was needed. No logins, no forms, nothing downloaded was run.

## 1. Ideal Vacuum 12 in. cube: the face opening (E2)

Not published anywhere we can reach, so the number below is an estimate.

- **Still blocked.** idealvac.com shows Cloudflare's "Sorry, you have been blocked" through the Pi (09:32Z), and
  `/files/cad/P107540.step` returns HTTP 403 through the Pi and from the runner directly.
- **The frame's STEP exists but was never archived.** The archived product page (2026-04-10) offers "P107540 3D CAD
  Parasolid Model.step". The Wayback Machine has no capture of it, nor of the 12x12 plate or coupler STEP files.
- **The only frame drawing is the 6x6x6** (manual IdealCUBE-6x121416 V1.1, Figure 1, archived 2025-08-11): "A 6x6x6
  Vacuum Cube Frame is machined as an exact 6.000” cube", with a square face opening dimensioned "104.14 / 4.100"
  and corners "R.500". Scaled from the figure, each rail is 0.65 in of flat face plus a 0.30 in sealing taper, 0.95 in
  in all.
- **The brochure (2019 v2) gives the 12x12x12** as '"Plate to plate" Inner Dimensions 11.4" x 11.4" x 11.4"',
  "1380 in3 (22.6 Liters)", mass "8.4 lbs (3.8 kg)" (6x6x6: 5.4 in, 134 in3, 3.7 lb).

| Estimate of the 12 in. frame's face opening | Opening |
|---|---|
| Ideal Vacuum's render of the frame (`VacuumFrame12X12_VC-01-913_01.jpg`): flat rail face 0.57-0.66 in of the 12 in. face, plus the 6x6x6's 0.30 in taper | 250-260 mm (9.9-10.2 in) |
| The same 0.95 in rail as the 6x6x6 | 256.5 mm (10.1 in) |
| The brochure's volume with square-section rails (the same model gives the 6x6x6's opening as 4.085 in against the drawn 4.100 in) | 243 mm (9.58 in) |

**Round 3's retry (10:34Z) read three more archived manuals**: the Cube Plate Installation Manual (V 1.3.2, archived
2025-08-11, and V1.2, archived 2023-08-10) and the Cube Coupling Kit manual (V 1.02, archived 2025-08-03). None gives
the 12 in. frame's face opening: their figures are renders without dimensions. So the estimate below stands.

The volume fits 1.21 in square rails or 0.95 in wide by about 1.6 in deep rails equally well, so it does not settle
it; the render points to the second. **So the 247 mm cassette probably passes a face (most likely about 255 mm, 8 mm
to spare), but this is not confirmed.** Ask Ideal Vacuum for P107540's drawing or STEP by phone or e-mail before
relying on it. The edge-on fallback (the bare deck through 180.3 mm) is unaffected.

## 2. SCANLAB RTC4 software (L5, control)

- SCANLAB's download page (no login): "Latest RTC4 Software Release (2023-11-02)" and "Latest RTC4 Ethernet V2
  Software Release (2023-11-02)". The file is `RTC4_Software_2023-11-02.zip` (7.4 MB).
- In it: `Windows/RTC Files/RTC4DLLx64.dll` (689,664 bytes, 2023-10-27), `RTC4DLLx64.lib` and the signed
  `SLRTCDRVx64.SYS`. Readme.txt: "RTC4DLLx64.DLL 64-bit RTC4 dynamic link library (version number 460)" and drivers
  "for the 32-bit or 64-bit versions of the Microsoft operating systems WINDOWS 10 / 8 / 7 / Vista / XP". Windows 11
  is not named.
- RTC4 brochure dated 11/2026: "The RTC4 series of control boards is available with two different interfaces: PCI
  Express (RTC4 PCIe), Ethernet (RTC4 Ethernet)"; "Driver for Windows 10 (x64)". The RTC boards page lists RTC4 beside
  RTC5 and RTC6. No discontinuation notice; no price.

## 3. PicoScope 4824A (MON8)

Pico's own page with the currency set to US Dollar: **4824A US$2999**, "In stock. Available for despatch. Shipped
from Texas"; US$3135 with 4 probes. Same selector: 4424A US$1529, 4224A US$987.

## 4. Raspberry Pi HQ Camera (MON1)

The C/CS-mount camera is out of stock nearly everywhere; the M12 version is in stock.

| Seller | Item | Price | Stock |
|---|---|---|---|
| PiShop.us | HQ Camera CS | $55.00 | out of stock ("notified when this item is back in stock") |
| PiShop.us | HQ Camera M12 (SC0870) | $50.00 | In Stock |
| SparkFun | HQ Camera Module | $63.75 | BACKORDER |
| Digi-Key | SC1220 (also listed as 2648-SC0261-ND) | $50.00 | 0; "90 expected in stock on 28-Dec-2026"; lead time 26 weeks |
| Digi-Key | SC1221 M12; Seeed 101990642 | $50.00; $77.00 | 0; 0 |
| Micro Center, Vilros | no HQ camera body listed | | |

## 5. Acoustic emission (MON5)

| eBay listing | Price | Notes |
|---|---|---|
| PAC R15α, used ([406195794085](https://www.ebay.com/itm/406195794085)) | $899.00 or Best Offer | no preamp; ships from China, Dec 7-18; 60-day returns |
| PXR15I, new ([167907977766](https://www.ebay.com/itm/167907977766)) | $809.10 | 150 kHz resonant, built-in 40 dB preamp; China, Dec 7-21; 60-day returns |
| PXR15, new ([168624831133](https://www.ebay.com/itm/168624831133)) | $270.82 or Best Offer | sensor only; China, Dec 21-31; 14-day returns |
| PAC 1220A preamp, used ([265784120409](https://www.ebay.com/itm/265784120409)) | $169.00 + $14.96 | California, 2-4 days; no returns; 28 V phantom power |

Cheapest complete chain: PXR15 + 1220A, about $455 plus a 28 V supply and decoupler (estimate $50-100; connector match not checked), against
parts.csv's $800-2,000.

## 6. The Digi-Key reads round 2 missed

- **SDR-240-24:** the only one is Antaira Technologies' (a DigiKey Marketplace item from ICOMTECH), $209.00,
  "In-Stock: 179", "Will ship in approximately 5 days". "mean well SDR-240" returns 0 results.
- **67F075 is normally open**: "THERMOSTAT 75DEG C NO TO220-2", $10.75, In-Stock 74, 9 weeks. The normally closed part
  is **67L075**: "THERMOSTAT 75DEG C NC TO220-2", $8.11 each ($7.015 at 10), "In-Stock: 1,368", lead time 9 weeks,
  reset 50 °C, 0.5 A at 48 VDC.
- **SC0261:** Digi-Key now lists it as SC1220 (section 4).

## 7. BYU public pages

- **Purchasing cards** (updated July 22, 2026): "Per-transaction limit: Up to $3,500"; "Requests to increase the
  per-transaction spending limit above the maximum of $3,500 to purchase a good or service will not be approved";
  monthly $10,000 (individual card) or $20,000 (department custodian). Over $3,500 a card is "Not permitted. Create a
  Workday requisition instead." Prohibited: personal purchases, split transactions, gift cards, peer-to-peer payments
  (Venmo), independent contractors, hazardous materials, high-risk merchants (jewelry, pawn shops). **eBay and online
  marketplaces are not mentioned** on any public purchasing page read.
- **Laser safety:** Risk Management's program list names "Laser Safety", but the page
  (`risk.byu.edu/ehs/shp/laser-safety`) redirects to BYU's CAS sign-in, as does Radiation Safety. The Wayback
  Machine's captures (2020-2024) are redirects too. Laser registration, the LSO and Class 4 rules need a BYU login or
  a call to Risk Management.
