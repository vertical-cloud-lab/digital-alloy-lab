# Order list: rePowder data-capture integration (28 November 2026)

This prices the parts for the integration steps in this folder: a camera on the HMI, a camera on the furnace's
GU 500 panel, a switch on the HMI's Ethernet link, and an isolated tap on the ultrasonic generator's 0–10 V
power output. Prices were read on 28 November 2026, the Saturday after Black Friday. Some Amazon prices are sale
prices; where Amazon showed a struck-through list price, the JSON records it.

**How the pages were fetched.** Every vendor page went through the CubXL Pi, so requests left from BYU's campus
network (AS6510), not from the GitHub runner. 45 page loads went through the Pi:
- 23 with curl run on the Pi over Tailscale SSH ([`fetch_via_pi.py`](fetch_via_pi.py)): Adafruit, PiShop,
  CanaKit, the Ubiquiti store and Octopart.
- 21 Amazon pages in a fresh headless Chrome on the runner, with its traffic sent through an SSH SOCKS tunnel to
  the same Pi. Images and fonts were blocked and nothing was signed in to. The tunnel was closed and the browser
  profile deleted afterwards.
- 1 check of the tunnel's exit network.

Nothing was written on the Pi. Raw HTML is not committed.

**Bot checks: 4, all on curl.** Amazon answered curl with its automated-access page (HTTP 503), so Amazon was
loaded in the browser instead, with no checks in 21 loads. DigiKey answered with a Cloudflare challenge, and Mouser
and Arrow with 403. Their prices and stock below come from Octopart's offer tables, fetched through the Pi.

Every candidate, with URL, stock and fetch time, is in [`order_list_2026-11-28.json`](order_list_2026-11-28.json).

## Totals

| Group | Needs AMAZEMET's OK? | Subtotal |
|---|---|---|
| 1. HMI camera station | No | $90.76 |
| 2. GU 500 panel camera station | No | $60.85 |
| 3. HMI Ethernet switch | **Yes** | $31.42 |
| 4. STG1 0–10 V power tap | **Yes** | $118.56 |
| **All four** | | **$301.59** |

Before tax and shipping. Groups 1 and 2 ($151.61) can be ordered now. Order groups 3 and 4 ($149.98) only if
AMAZEMET agrees to a switch on the HMI link and a passive tap on the generator's X3 connector.

By vendor: Amazon $163.64, CanaKit $64.90, Adafruit $50.85, PiShop $7.90, Mouser $6.50, and $7.80 of resistors and
capacitors (DigiKey, Newark, Arrow).

## 1. HMI camera station (the Pi 5 is already there)

| Item | Pick | Price | Qty | Line total | Notes |
|---|---|---|---|---|---|
| H1 Matte anti-glare film, 15.6 in 16:9 | [Supershieldz 3-pack, 344 × 194 mm](https://www.amazon.com/dp/B08HSG4RNM) | $9.99 | 1 | $9.99 | Matte, no blue-light tint. The cut size is the cMT2166X's active area. Three films: the HMI, the GU 500 (P1) and a spare. 3.7★ (155) |
| H2 Camera Module 3 **Wide** (102°) | [CanaKit RSP-CAM-V3-WIDE](https://www.canakit.com/raspberry-pi-camera-module-3.html?defpid=4838) | $37.95 | 1 | $37.95 | The camera sits about 260 mm from the screen, so it needs the wide lens. PiShop and Adafruit list it at $38.50 but both are **out of stock** |
| H3 Pi 5 camera cable, 500 mm | [PiShop](https://www.pishop.us/product/camera-cable-for-raspberry-pi-5/) | $3.95 | 1 | $3.95 | 22-pin to 15-pin. Choose 500 mm |
| H4 11 in magic arm with super clamp, 1/4-20 | [NEEWER ST16C](https://www.amazon.com/dp/B0D1JTGYPC) | $22.94 | 1 | $22.94 | Clamps on the HMI's top edge, so the camera swings with the HMI. **The clamp must open to at least 30 mm**, because the HMI housing is 28 mm thick. The listing gives no jaw range. Put a rubber or felt pad on the jaws. 4.6★ (618) |
| H5 1/4-20 brass heat-set inserts | [40-pack](https://www.amazon.com/dp/B0DYPJKVML) | $8.94 | 1 | $8.94 | For the printed camera holder. Only 9 reviews |
| H6 6 × 3 mm disc magnets | [60-pack](https://www.amazon.com/dp/B0BW91ZTKZ) | $6.99 | 1 | $6.99 | Detent for the privacy flap. 4.6★ (1,886) |
| | | | | **$90.76** | |

Alternatives: the standard Camera Module 3 (66°) for H2, at [CanaKit](https://www.canakit.com/raspberry-pi-camera-module-3.html?defpid=4838)
($26.95) or [PiShop](https://www.pishop.us/product/raspberry-pi-camera-module-3/) ($29.25, in stock), if the
camera can sit farther back. [SmallRig 11 in magic arm](https://www.amazon.com/dp/B0F5VJDVT9) ($25.59) for H4.
Avoid blue-light and privacy films for H1: they tint or darken the screen.

## 2. GU 500 panel camera station (the Pi 5 is already there)

| Item | Pick | Price | Qty | Line total | Notes |
|---|---|---|---|---|---|
| P1 Small anti-glare film (LCD about 110 × 60 mm) | A spare film from H1's 3-pack, cut down | $0.00 | – | $0.00 | If buying separately: [Supershieldz 3-pack for Fire 7](https://www.amazon.com/dp/B0B1VT1JFS) ($9.99), cut to size |
| P2 Camera Module 3 (standard, 66°) | [CanaKit RSP-CAM-V3](https://www.canakit.com/raspberry-pi-camera-module-3.html?defpid=4838) | $26.95 | 1 | $26.95 | Same CanaKit order as H2. PiShop has it at $29.25, in stock |
| P3 Pi 5 camera cable, 500 mm | [PiShop](https://www.pishop.us/product/camera-cable-for-raspberry-pi-5/) | $3.95 | 1 | $3.95 | |
| P4 Magnetic base with adjustable arm, 1/4-20 | [ARKON RMSMAG1420](https://www.amazon.com/dp/B08MTBQLKK) | $29.95 | 1 | $29.95 | Holds to the painted steel cabinet. The listing doesn't say the magnet is coated, so put a felt pad under it |
| | | | | **$60.85** | |

Alternative for P4: a [rubber-coated 60 lb magnetic base with a ball head](https://www.amazon.com/dp/B08MQBXLSD)
($24.99). It won't mark the paint, but it has no arm, so the camera can't stand off as far.

## 3. HMI Ethernet switch: only with AMAZEMET's OK

| Item | Pick | Price | Qty | Line total | Notes |
|---|---|---|---|---|---|
| N1 5-port gigabit switch | [TP-Link TL-SG105](https://www.amazon.com/dp/B00A128S24) | $12.94 | 1 | $12.94 | Unmanaged, metal case. TP-Link supplies a 5 V adapter with it, though the listing text didn't say so. 4.7★ (130,544) |
| N2 USB-C 5 V adapter | Not needed | $0.00 | – | $0.00 | Both switches come with an adapter |
| N3 Cat6 patch cables, 2 × 1 ft | [Cable Matters 5-pack, 1 ft](https://www.amazon.com/dp/B00C4U030G) | $9.99 | 1 | $9.99 | |
| N3 Cat6 patch cable, 6 ft | [Cable Matters, 6 ft](https://www.amazon.com/dp/B0CP9XGZKM) | $8.49 | 1 | $8.49 | |
| | | | | **$31.42** | |

The other switch priced: [Ubiquiti Switch Flex Mini](https://store.ui.com/us/en/products/usw-flex-mini) at $29,
in stock. It runs off PoE or USB-C, and its page says the USB-C adapter is included. Also the
[TP-Link LS1005G](https://www.amazon.com/dp/B0863M7C1L) at $7.99, in a plastic case. If the HMI's Ethernet port turns
out to be free, no switch is needed.

## 4. STG1 0–10 V power-output tap: only with AMAZEMET's OK

| Item | Pick | Price | Qty | Line total | Notes |
|---|---|---|---|---|---|
| A1 DB15 male + female pass-through, screw terminals | [Electronics-Salon DIN-rail module MD-D212T-1](https://www.amazon.com/dp/B00SUKB2GS) | $22.99 | 1 | $22.99 | Male and female 2-row DB15, terminals for all pins, DIN rail. 87 × 49.5 × 43 mm. Only 19 left |
| A2 USB isolator | [Adafruit 2107](https://www.adafruit.com/product/2107) | $34.95 | 1 | $34.95 | **Micro-USB in** (to the Pi), **USB-A out** (isolated side). The isolated 5 V supply gives **100 mA**. Low and full speed only (12 Mbps). 64 in stock |
| A3 MCP2221A USB-to-I2C breakout | Adafruit 4471, from [Mouser 485-4471](https://www.mouser.com/ProductDetail/485-4471) | $6.50 | 1 | $6.50 | **USB-C** connector, STEMMA QT, 3 V regulator. Out of stock at Adafruit; Mouser had 919 |
| A4 ADS1115 16-bit ADC | [Adafruit 1085](https://www.adafruit.com/product/1085) | $14.95 | 1 | $14.95 | STEMMA QT. In stock |
| A5 STEMMA QT cable | [Adafruit 4399, 50 mm](https://www.adafruit.com/product/4399) | $0.95 | 1 | $0.95 | The 100 mm (4210) is out of stock. 50 mm is enough inside one box |
| A6 200 kΩ 0.1 % metal film | Vishay CMF55200K00BEEB, DigiKey CMF200KHBCT-ND | $1.57 | 2 | $3.14 | Top of the 3:1 divider (0–10 V to 0–3.3 V). 10,877 at DigiKey. One is a spare |
| A6 100 kΩ 0.1 % metal film | Vishay CMF55100K00BEEB, [Newark](https://www.newark.com/search?st=CMF55100K00BEEB) | $2.06 | 2 | $4.12 | Bottom of the divider. Octopart showed no DigiKey offer |
| A6 100 nF film capacitor | KEMET R82DC3100AA50K, [Arrow](https://www.arrow.com/en/products/search?q=R82DC3100AA50K) | $0.27 | 2 | $0.54 | 63 V, 5 mm pitch. Low-pass filter at the ADC input |
| A7 Shielded 2-conductor 22 AWG cable | [UL2464, 25 ft](https://www.amazon.com/dp/B0D9JV41J7) | $13.99 | 1 | $13.99 | From the DB15 terminals to the ADC box. 25 ft is the shortest sold |
| A8 USB-A to micro-B, 6 ft | [Amazon Basics 2-pack](https://www.amazon.com/dp/B071S5NPG9) | $9.64 | 1 | $9.64 | Pi to isolator. A data cable (480 Mbps) |
| A8 USB-A to USB-C, 0.5 ft | [Short data cord](https://www.amazon.com/dp/B01CZVEUIE) | $6.79 | 1 | $6.79 | Isolator to MCP2221A. Listed as a data cord, not charge-only |
| | | | | **$118.56** | |

The chain is: Pi USB-A → 6 ft cable → isolator (micro-USB in, USB-A out) → short cable → MCP2221A (USB-C) →
STEMMA QT → ADS1115 → divider → A1's terminals.

- **If X3 is a 3-row HD-15,** use the [3-row DIN-rail module](https://www.amazon.com/dp/B0FJ8PRTBT) ($17.49) for A1
  instead.
- **A cheaper isolator** is the [Jhoinrch ADuM3160](https://www.amazon.com/dp/B0DNMMXS5D) ($18.99). It also runs at
  12 Mbps, and its isolated 5 V gives 400 mA, with 1500 V power and 2500 Vrms signal isolation. It has USB-A on both
  sides and ships with an A–A cable, so it would need a 6 ft A–A cable instead of A8's micro-B one.
- **For the resistors and capacitor,** Mouser has the 200 kΩ at the same $1.57 (71-CMF55200K00BEEB). Checking the
  other two there would save two tiny orders. Three 100 kΩ resistors, two in series for the top leg, also make 3:1,
  with matched temperature drift, from one part number.
- **The other USB-to-I2C option,** Adafruit's FT232H (2264, $14.95), is also out of stock.

## Check before ordering

1. **X3's rows and gender.** Is X3 a 2-row DB15 (DA-15) or a 3-row HD-15, and which gender is on the generator and
   which on its cable? A1 has both genders, but the row count picks the part. Read it from a photo or the nameplate,
   and don't unplug anything without AMAZEMET's OK. Which pins carry the power output and its 0 V is in SONICTECH's
   manual (pp. 21–27). That isn't needed to order, only to wire.
2. **Whether the HMI and panel Pis already have cameras.** Both Pis timed out over SSH today, so this wasn't
   checked. If the HMI Pi has a standard Camera Module 3, move it to the GU 500 station and skip P2.
3. **The super clamp's jaw range** (H4) must reach 30 mm.
4. **Whether the HMI's Ethernet port is free.** This is question 1 for AMAZEMET. If it is free, skip N1 and plug the
   Pi straight in.
5. **Prices.** They are from the Saturday after Black Friday and will move. Check stock on the two items flagged out
   of stock elsewhere (H2, A3) on the day you order.
