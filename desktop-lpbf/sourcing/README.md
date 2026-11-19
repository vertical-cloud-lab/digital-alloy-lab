# Used, surplus and reseller options for the desktop LPBF parts (2026-11-19)

Checked on 2026-11-19 between 19:57 and 20:10 UTC, through the lab's CubXL Pi (BYU network), for [PR 266](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/266) and issue #260. Every row is in [`listings.csv`](listings.csv), with its URL and fetch time. These are asking prices from listings. No seller was contacted, nothing was bought, and listings change daily.

## Short answer

- **The laser class this machine needs is on the used market, in the US, for about a tenth of the new price.** IPG quoted about $23k for a new 500 W single-mode YLR, with 10–12 weeks after the order ([`../quotes/ipg-ylr-500-u3-sm-ac.md`](../quotes/ipg-ylr-500-u3-sm-ac.md)). On eBay:
  - three IPG **YLR-400-SM-EOS** 400 W single-mode lasers are listed in the US, at **$1,299.99**, $2,099.99 and $3,995. The first two come from a large surplus seller and have free returns;
  - a refurbished YLR-200-SM-EOS is $2,450, and a YLR-200-AC-Y11 single-mode unit is $2,499.99 with free returns (both US);
  - a **YLR-500-AC** single-mode unit, air-cooled like the quoted one, is $4,999.90 plus $1,953 shipping from South Korea;
  - two water-cooled YLR-500-WC units described as single-mode are $6,800 and $7,000 plus $500 from China.

  US sellers ship in days, not 10–12 weeks. Several are under the $3,500 above which BYU needs a purchase order (per the quote note).
- **400 W is inside the 300–500 W band in README §3.2.** The "-EOS" suffix and the "IPG Laser GmbH" plate in one title suggest these came out of EOS LPBF machines; EOS's M 290 runs one 400 W Yb fiber laser (per the refurbished M 290 listing below). If so, they are the laser class commercial LPBF uses. None of the listings states hours, cooling or the fiber's condition, and an OEM variant may not run outside its host machine. See [the checks](#before-buying-a-used-laser) before buying.
- **Scan heads, scan cards and lenses are cheap used, too.**
  - SCANLAB heads for fiber lasers: an intelliSCAN III 20 at 1080 nm, new in an open box with a 30-day warranty and free returns, is **$1,500**. hurrySCAN 25 heads rated to 1500 W at 1064 nm are $1,200–1,286. A new-in-box hurrySCAN 20 at 1080 nm is $2,750. All are in the US.
  - Scan cards: an RTC5 PCIe card with the 3D option is $1,499.99, and an RTC6 PCIe card is $2,350 (both US).
  - An f = 254 mm, 1064 nm F-Theta-Ronar lens is $99.99. An IPG collimator is $495.
- **Put together,** a used US set comes to about **$4.9k–5.8k plus the laser's freight**: the $1,299.99 laser, the $1,500 head, an RTC5 or RTC6, the lens and the collimator. The same five BOM lines (L1, L3, L5, L6 and C1) run $4.3k at the BOM's low end, which needs a PRC laser and a marking galvo, and $44k at its high end. README §6 put a realistic new US build of the laser, head and controller at $32–48k.
- **Other BOM lines:**
  - trace-O₂ analyzers are $650–779 used, against $1,271–2,091 on line G6;
  - dry scroll pumps are $1,150 used or $3,500 rebuilt, against the ~$4,000 high option on G2;
  - a 1.5 kW Ophir thermal head is $454 from China. Line T1 needs a ≥ 500 W head, and the listing has no meter.
- **Used commercial desktop LPBF machines are in Europe, and they aren't cheaper than new US-market ones.**
  - An EOS M 100 (dental, 2016) is €45,000 in Bosnia and Herzegovina.
  - An SLM 125 HL (2016) is €61,000 in Germany.
  - A TRUMPF TruPrint 1000 (2022, 500 laser hours) is €90,000 in Romania.
  - A refurbished EOS M 100 in the Netherlands, an ORLAS Creator and a ProX 100 Dental are price on request.

  All of those are before VAT, crating, freight, import and the maker's recommissioning. New, the AO Metal A30 is from $59k and the Xact XM200C is $65k (README §2.2). eBay had no metal LPBF machines; searches for them returned cameras and paper printers.
- **No IPG refurbished program turned up**, and the one online reseller of new IPG lasers I found charges more than IPG direct: a YLR-400-WC-Y14 is $39,935 there.

## What I checked, and how

| Where | What | Result |
|---|---|---|
| eBay (US site) | 32 live searches: IPG YLR-200/300/400/500, single-mode fiber lasers, SPI redPOWER, Raycus, SCANLAB hurrySCAN/intelliSCAN/basiCube/RTC5/RTC6, Raylase, Cambridge Technology, f-theta lenses, IPG collimators, Ophir heads, trace-O₂ analyzers, dry scroll pumps, gloveboxes, EOS M 100, TruPrint 1000, Sisma MYSINT, metal 3D printers | the rows in [`listings.csv`](listings.csv); every result card was saved locally |
| eBay sold listings | realized prices | **not available:** eBay now sends sold-listing searches to its sign-in page |
| Machineseeker, resale.info, Multistation | used LPBF machines | 8 machines, 4 with prices |
| Surplus Record, CAE Online, Next Day Automation | used lasers and scan heads | 3 rows |
| An online reseller shop for new IPG lasers | new and refurbished YLR prices | new only; every refurbished option shows no price |
| Web search | IPG refurbished program, dealers of used SM lasers | no IPG program found |
| Machinio, LabX | used lasers and machines | not reached: their search URLs returned 404 through the tunnel |

**Method.** The three atomizer camera Pis were offline, so the tunnel went through the CubXL Pi (exit network: BYU, AS6510), as in the byu-vcl Onshape rig.
- I used that rig's script to start headed Chrome on a virtual display on the runner, with a SOCKS tunnel through the Pi.
- **eBay served its error page whenever Playwright drove the navigation.** It loaded normally when the URL was typed into Chrome's address bar with `xdotool`. So [`scripts/xnav.sh`](scripts/xnav.sh) types each search or item URL and scrolls with the mouse wheel. [`scripts/cdp_eval.py`](scripts/cdp_eval.py) then reads the result cards with a single `Runtime.evaluate` over the DevTools socket, without attaching Playwright.
- [`scripts/batch.py`](scripts/batch.py) ran the searches in [`scripts/ebay-queries.txt`](scripts/ebay-queries.txt), about 15 s apart.
- **After about 40 page loads eBay rate-limited the session.** It served its error page for the rest of the run, so the item pages ([`scripts/items.py`](scripts/items.py)) were not opened. Every eBay row is therefore read from its search-result card: title, price, condition, shipping, location, returns and seller feedback. Seller names are left out.
- Dealer and marketplace pages were read in headless Chrome through the same tunnel, with [`../cad/fetch_pages.py`](../cad/fetch_pages.py).

## 1. Laser (BOM line L1)

IPG's model names give power, beam mode and cooling. SM means single-mode and MM means multimode. AC is air-cooled and WC is water-cooled. Only single-mode gives the ~75 µm spot in README §3.2. Water cooling brings back line L2 (a chiller, up to $3k).

| Model | Power | Mode | Cooling | Condition | Price (shipping) | Located | Returns |
|---|---|---|---|---|---|---|---|
| YLR-400-SM-EOS | 400 W | SM | not stated | used | **$1,299.99** (freight) | US | free returns |
| YLR-400-SM-EOS | 400 W | SM | not stated | used | $2,099.99 (freight) | US | free returns |
| YLR-400-SM-EOS | 400 W | SM | not stated | used | $3,995 (freight) | US | – |
| YLR-200-SM-EOS | 200 W | SM | not stated | refurbished | $2,450 (freight) | US | – |
| YLR-200-AC-Y11 | 200 W | SM | air | used | $2,499.99 (+$99.99) | US | free returns |
| YLR-200-AC-Y11 | 200 W | SM (same model) | air | new, open box | $5,999 (pickup) | US | – |
| YLR-300-AC | 300 W | SM | air | used | $2,999.90 (+$1,265.80) | South Korea | – |
| **YLR-500-AC** | 500 W | SM | air | used | $4,999.90 (+$1,953) | South Korea | – |
| YLR-500-WC (14 µm core) | 500 W | SM per title | water | used, "tested OK" | $6,800 / $7,000 (+$500) | China | – |
| YLR-500-WC | 500 W | not stated | water | used | $1,850 | US | – |
| YLR-400-WC (2018, 2020) | 400 W | not stated | water | used | $5,000 each, 4 listed (freight) | US | – |
| YLR-400-WC-Y14 + collimator | 400 W | not stated | water | new, open box | $21,999.99 (pickup) | US | – |
| *New, for comparison:* YLR-500-U3-SM-AC | 500 W | SM | air | new (IPG quote) | ~$23k, 10–12 weeks ARO | – | – |

Also seen, and not suitable:
- multimode YLR-500-MM-WC units at $2,900–4,800, mostly from China. Their larger core won't give the spot;
- SPI redPOWER units of 50–100 W only;
- a 100 W YLR-100-SM-C at $3,900;
- IPG YLR-1500-SM and YLR-2000-SM units from China at $12k and $20k.

**Where the 200 W units stand.** README §3.2 says 200 W has made 99 % dense AlSi10Mg (Kempen et al. 2011) and that 300 W gives headroom. A $2.5k 200 W single-mode unit is therefore enough for single tracks on Al (phase 1). The 400 W units cover the whole CW route.

**Two ways to use this, for Sterling to choose:**
1. **A returnable bridge.** Buy one of the two US YLR-400-SM-EOS units that have free returns, and test it within the return window ([checks below](#before-buying-a-used-laser)). This starts the CW route without waiting 10–12 weeks. If it passes, the IPG order can wait until the go/no-go point. If it fails, send it back. Either way, a used laser for early tracks protects the new one.
2. **The closest match to the quote.** The air-cooled YLR-500-AC from South Korea is the same power, mode and cooling as the quoted unit, for about $7k delivered, but with import paperwork and no stated returns. The open question about PRC vendors (README §7 Q1) concerns the vendor, so check whether a Korean or Chinese seller of an IPG-built unit is acceptable on the funds.

## 2. Scan head, controller and optics (L3, L5, L6, C1)

| Line | Item | Condition | Price (shipping) | Located | Notes |
|---|---|---|---|---|---|
| L5 | SCANLAB intelliSCAN III 20, 1080 nm | new, open box; 30-day warranty | **$1,500** (+$27.71) | US | free returns; the seller lists several. A used one with a 1:1.6 expander is $899.10 |
| L5 | SCANLAB hurrySCAN 20, 1080 nm | new, open box | $2,750 | US | |
| L5 | SCANLAB hurrySCAN 25, 1064 nm, "up to 1500 W", with optics | used | $1,286.29 (+$53.52) | US | |
| L5 | SCANLAB hurrySCAN 25, 1500 W at 1064 nm | used | $1,200 | US | the dealer's own site adds 1/2/3-year warranties for $180/$276/$360 and says it isn't an authorized SCANLAB distributor |
| L5 | SCANLAB intelliSCAN se 20, SL2-100 | used | $5,840 | US | auction-house listing |
| C1 | SCANLAB RTC5 PCIe, 3D + 2nd head + marking-on-the-fly options | used | $1,499.99 (+$20.36) | US | |
| C1 | SCANLAB RTC6 PCIe | used | $2,350 (+$6.55) | US | Chinese sellers list RTC6 cards at $2.4–5.1k |
| L6 | LINOS F-Theta-Ronar f = 254 mm, 1064 nm | used | $99.99 | US | free returns; others $384.99–749.99 |
| L3 | IPG collimator P30-001277 | used | $495 | US | beam diameter not in the card |

Against the BOM:
- **L5** is $419–12,000, where the high end is a quoted basiCube 20;
- **C1** is $60–6,000;
- **L6** is $486–2,500.

What to check:
- **Interface.** The head and the card have to speak the same digital protocol (XY2-100 or SL2-100). Some intelliSCAN heads use SL2-100, as the $5,840 listing does. Confirm it on the head's label and the card's datasheet before buying either.
- **Power rating.** The heads need mirrors coated for 1064–1080 nm and rated for 300–500 W CW. The 1080 nm intelliSCAN and hurrySCAN 20 heads are fiber-laser variants, and the hurrySCAN 25 is listed to 1500 W. The 14 mm hurrySCAN at 250 W in `listings.csv` is too low.
- **Lens rating.** The f = 254 mm lenses are marking lenses with no CW rating, the same caveat as line L6.
- **Missing pieces.** Most heads need their own DC supply, which the listings don't include. The RTC cards need SCANLAB's driver and DLL: ask SCANLAB whether a second-hand card can register for them.

## 3. Other BOM lines

| Line | Item | Condition | Price (shipping) | Located | BOM range |
|---|---|---|---|---|---|
| G6 | Teledyne 3190 trace-O₂ analyzer, 4–20 mA | used | $779 | US, free returns | $1,271–2,091 |
| G6 | Alpha Omega Series 3000 trace-O₂ analyzer | used | $650 (+$27.65) | US | |
| G6 | AMI 2010BX trace-O₂ analyzer with sensor kit | new, open box | $2,300.93 | US | |
| G2 | Agilent IDP-3 dry scroll pump | used | $1,149.99 (+$134.59) | US | high option ~$4,000 |
| G2 | Edwards XDS10 dry scroll pump, rebuilt, 64 h | used | $3,499.95 (+$200) | US | |
| T1 | Ophir L1500W thermal head (no meter) | used | $454 (+$45) | China | $1,690–4,000 |

A used trace-O₂ analyzer usually needs a new sensor cell, so budget for one and check the range against < 100 ppm. Teledyne 3000TA analyzers run $4.5–10.3k on eBay; one comes with a 2-year warranty from a US reseller at $8,770.96.

## 4. Used commercial machines (the go/no-go fallback)

| Machine | Year | Laser, build | Price | Located | Notes |
|---|---|---|---|---|---|
| EOS M 100 (dental) | 2016 | 200 W, Ø100 × 95 mm | €45,000 ONO + VAT | Bosnia and Herzegovina | 230 V 16 A, 570 kg. A dental machine, so ask which materials and software licences transfer |
| EOS M 100, refurbished | – | 200 W, 100 × 100 × 95 mm | on request | Netherlands | remanufacturer; transport, installation and maintenance plans offered |
| EOS M 100 | 2016 | – | on request | Finland | |
| SLM Solutions SLM 125 HL | 2016 | 400 W, 125 × 125 mm | €61,000 ONO + VAT | Germany | 6,250 h; 400 V 3-phase, 32 A; 800 kg |
| TRUMPF TruPrint 1000 | 2022 | 200 W, Ø98 × 100 mm | €90,000 ONO + VAT | Romania | 5,000 h, 500 laser hours; 1.68 m tall |
| OR Laser ORLAS Creator | 2018 | 250 W, Ø100 × 100 mm | on request | Germany | |
| 3D Systems ProX 100 DMP Dental | – | – | on request | Europe | CoCr dental version |
| *For scale:* EOS M 290, refurbished | – | 400 W, 250 × 250 × 325 mm | on request | Netherlands | not desktop |

Before comparing these with new machines, add:
- crating, freight and import;
- the maker's recommissioning, and any licence transfer;
- a glovebox if O₂ has to be below 100 ppm (README §2.2 has the TruPrint 1000 at ≤ 3,000 ppm without one);
- for the SLM 125, 3-phase power.

None of these listings mentions plate heating, so ask about it first, as README §5 says for the new ones. **The used route doesn't beat the A30 ($59k new) on price.** It is worth a look only if a specific machine, such as the M 100 at €45k, comes with the materials and software we need.

## 5. Resellers of new lasers

- **IPG sells direct in the US, and I found no IPG refurbished or certified pre-owned program.** Web searches turned up IPG's retrofit offer (2009) and other makers' pre-owned programs (Trotec, OMTech, Candela), but nothing for IPG.
- **One online reseller lists new IPG lasers above IPG's direct price.** It asks $39,935 for a YLR-400-WC-Y14, $45,795 for a YLR-700-WC-Y14 and $54,795 for a YLR-1000-WC, with a 30-day money-back guarantee and 2–3 day shipping. Its YLR-500-AC and every "Refurbished" option show $0.00, so they aren't actually priced.
- **A new-in-box YLR-400-WC-Y14 with a collimator is $21,999.99 on eBay**, which is about IPG's quote for a new 500 W unit. Its mode isn't stated.
- **Still worth asking:** nLIGHT (US-made; a 500 W single-mode CFL-500 is listed on FindLight, whose page returned 404 through the tunnel) and IPG itself, whether it has a demo or stock unit that ships sooner than 10–12 weeks.

## Before buying a used laser

Ask the seller:
- for the serial number, to give to IPG. Ask IPG whether the unit is an OEM variant (the -EOS units especially), whether it runs stand-alone through its standard interface, and what an evaluation or repair costs;
- whether it is air- or water-cooled (the EOS units may be water-cooled, since EOS machines carry a chiller);
- the delivery fiber's length, and what it ends in: QBH, collimator, or cut. **A cut or kinked fiber is an IPG repair;**
- for the operating hours, if the seller can read them, and a power test at several set points, as a video or a log;
- for the return terms, in writing.

On arrival, inside the return window:
1. Inspect the fiber end and check the guide laser.
2. Fire into a beam dump at 10–100 % with a power meter, and plot power against set point.
3. Read the alarm and status registers over RS-232 or Ethernet.
4. If a profiler is available, check M²: the 75 µm spot depends on it.

The lab still owes the same safety work as for a new laser: BYU Laser Safety Officer registration, and the interlock chain in README §3.7. Back-reflection protection isn't stated for any of these units. It matters for Al (README §3.2), so ask IPG with the serial number.

## Not done

- **eBay item pages were not opened,** because eBay rate-limited the session. Cooling, hours, fiber, accessories and interface come only from titles, or are not stated.
- **No sold-price history:** eBay needs a sign-in for it, and I didn't create an account.
- **No seller or IPG contact, no quotes, nothing bought.** BYU's rules for buying on eBay or from surplus dealers, such as card versus PO and used equipment on these funds, are for BYU purchasing to answer.
- **Not searched:** Machinio and LabX (404 through the tunnel), MOPA engravers for the student's route (README §1b.1), and gloveboxes (eBay rewrote the query to "glove box insert").
- **Prices change.** Listings come and go. Re-run [`scripts/batch.py`](scripts/batch.py) with the same queries to refresh them.

## Files

| File | What it is |
|---|---|
| [`listings.csv`](listings.csv) | 42 listings: category, BOM line, item as listed, condition, price, shipping, location, returns, seller type, URL, fetch time and fit notes |
| [`scripts/`](scripts/) | the eBay search and extraction scripts: typed navigation with `xdotool`, a raw-CDP read and the query list |
