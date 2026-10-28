# Argon regulator for the rePowder atomizer

The regulator on the atomizer's argon cylinder is borrowed. It's a Harris 9296
([#163](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/163)). This page covers:

- what a replacement has to do;
- what to buy, and where, new or second-hand;
- the Amazon regulator, which still has to go back.

The aim is that the next purchase doesn't repeat the Amazon one. It was first written on 20 Oct
2026 on a [byu-vcl branch](https://github.com/vertical-cloud-lab/byu-vcl/tree/claude/issue-289-20261020-1938),
when this issue was byu-vcl#289. The eBay and supplier search was added on 28 Oct 2026.

## Recommendation

**Buy a new Harris 9296SS-250-580** (Harris item 3302689) from a Harris distributor. It's
**$553.19 at [Weldingmart](https://weldingmart.com/products/harris-9296ss-250-580-two-stage-argon-helium-nitrogen-regulator-3302689)**,
the same price on 28 Oct as on 20 Oct. It's the borrowed model with a stainless-steel diaphragm
instead of neoprene. If you'd rather have exactly the borrowed model, the **9296-250-580** (item
3302609) is
[$516.00](https://weldingmart.com/products/harris-9296-250-580-general-purpose-two-stage-argon-helium-nitrogen-regulator-3302609).
Either way, add a **1/4" NPT male × 6 mm push-to-connect** fitting for the outlet.

**Don't buy this one on eBay.** On 28 Oct, eBay had dozens of Harris 9296s, most between $50 and
$500, but only one was the 250 psi argon version. That one is used, ships by freight from Canada, and the
seller takes no returns. The rest were 125 or 150 psi versions, regulators for other gases, or
listings that didn't give the range. A used regulator also has an unknown history, and the best
any of these sellers offers is a 30-day return. Weldingmart lists a 7-year warranty for a new one.
The details are under [eBay](#ebay).

## What it has to do

| Requirement | Value | Source |
| --- | --- | --- |
| Gas | Argon, 5N (99.999 %) | 17 Sept 2026 install call with AMAZEMET |
| Delivery pressure | **8 bar (116 psi) at the machine, adjustable.** AMAZEMET's engineer asked for a 0–10 bar regulator, not a welding regulator: those are "usually set to three bars and you can only set the flow", and the machine's pneumatics need the higher pressure | 17 Sept call |
| Flow | Up to 100 L/min (212 SCFH), only while purging | AMAZEMET's facility list, [byu-vcl#41](https://github.com/vertical-cloud-lab/byu-vcl/issues/41#issuecomment-4225003786) |
| Inlet | CGA 580, the standard US argon cylinder valve | |
| Outlet | Into the 6/4 mm push-fit line to the T on the back of the machine, whose two 6/4 mm ports feed the furnace and the chamber-fill valve | 17 Sept call |
| Cylinders | One regulator per cylinder, no manifold. The booth may hold at most two argon or nitrogen cylinders, not manifolded, each on its own equipment, and no dewar. Under that limit no oxygen detection is needed | BYU safety review, 8 Oct 2026 ([byu-vcl#271](https://github.com/vertical-cloud-lab/byu-vcl/pull/271)) |

In practice that means:

- **Two-stage.** Outlet pressure stays put as the cylinder drains. A single-stage regulator's
  outlet creeps up as the cylinder empties, so it has to be reset.
- **A delivery range that reaches 116 psi with room to spare.** A 0–125 psi model would have to
  run at the very top of its spring.
- **CGA 580 inlet.**
- **Preferably a stainless-steel diaphragm,** for 5N argon. Neoprene lets a little air and
  moisture through into the gas. The plastic line to the machine probably lets in more than the
  diaphragm does, so this matters less than the first three points.

## The borrowed regulator

From the photos on #163:

- **Model:** Harris 9296 "Multi-Stage" (Harris's name for its two-stage design), marked for
  Ar/He/N2 service. "CGA E-4" on the label is the Compressed Gas Association's standard for gas
  pressure regulators, not a fitting.
- **Gauges:** 0–4000 psi on the inlet (USG BU-2581-AM). 0–400 psi on the delivery side (USG
  CU-2581-HF), reading about 800 kPa, i.e. the 8 bar the machine needs.
- **Outlet:** a push-to-connect fitting screwed straight into the low-pressure port.

That matches the **9296-250-580**. It's the only argon version that ships with a 0–400 psi
delivery gauge and a 1/4" NPT outlet. The 125 psi version has a 0–150 psi gauge and a 5/8"-18
outlet. The label says "9296", not "9296SS", so it most likely has the neoprene diaphragm. The
delivery-pressure number cut off at the end of the label should read 250 psig.

**Reading a 9296 part number.** `9296[SS]-<max delivery psig>-<CGA inlet>`, where `SS` means a
stainless-steel diaphragm. So `9296SS-250-580` is a stainless-diaphragm unit that delivers up to
250 psig from a CGA 580 (argon, helium, nitrogen) cylinder. Listings ending in `-320` (CO2),
`-350` (hydrogen, methane), `-510` (acetylene, propane) or `-540` (oxygen) are for other gases and
won't fit an argon cylinder. A listing that just says "9296" tells you nothing about the range.
Look for the "max. delivery pressure" on the label, or the delivery gauge in the photos: the 250 psi
version has a 0–400 psi gauge, and the 125 psi version a 0–150 psi gauge. Gauges get swapped, so
the label is the better guide.

## New, from a Harris distributor

Both 250 psi versions share the following, from Weldingmart's spec tables:

- Two-stage, brass body
- CGA 580 inlet, 3000 psig maximum inlet
- 0–250 psig delivery range, with a 0–400 psi delivery gauge
- 1/4" NPT female outlet
- Cv 0.15
- Internal relief valve
- Outlet changes 0.04 psi per 100 psi drop in cylinder pressure
- 7-year warranty

| Model | Harris item | Diaphragm | Weldingmart |
| --- | --- | --- | --- |
| **9296SS-250-580** (recommended) | 3302689 | stainless steel | **$553.19** (list $631.22), 28 Oct |
| 9296-250-580 (same as the borrowed one) | 3302609 | neoprene | $516.00 (list $588.77), 28 Oct |
| 9296-125-580 / 9296SS-125-580 (not recommended) | 3302608 / 3302688 | neoprene / stainless | $448.36 / $500.75, 20 Oct |

**Why not the 125 psi versions.** 116 psi is 93 % of their range. Their outlet is also a
5/8"-18 RH inert-gas hose thread rather than 1/4" NPT, which needs another adapter before a push
fitting
([125](https://weldingmart.com/products/harris-9296-125-580-general-purpose-two-stage-argon-helium-nitrogen-regulator-3302608),
[125 SS](https://weldingmart.com/products/harris-9296ss-125-580-general-purpose-ss-diaphragm-two-stage-argon-heliumnitrogen-regulator-3302688)).

**Flow.** Cv 0.15 is comfortably enough for the 212 SCFH purge peak. A rough choked-flow estimate
(q ≈ 640 · Cv · P₁ / √(G·T), argon G = 1.38, 530 °R) gives about 900–1,300 SCFH if the second
stage is fed at 250–350 psig, which is 4–6 times the peak. It's also the same flow rating as the
regulator on the cylinder now.

**Other places to get it.** These were checked from the lab Pi on 28 Oct:

- **Airgas** lists the 9296-250-580 as
  [HCL3302609](https://www.airgas.com/product/Gas-Equipment/Regulators/Specialty-Gas-Regulators/p/HCL3302609),
  but shows no price online.
- **Grainger** doesn't list the 9296. Its one Harris two-stage CGA 580 cylinder regulator
  (chrome-plated brass, neoprene diaphragm, 1/4" NPT male outlet) was $569.50.
- **Cyberweld** doesn't carry the 9296.
- **Zoro** blocked the Pi's browser as a bot, so it wasn't checked.
- **Norco (local)** was suggested for a Victor two-stage regulator in
  [byu-vcl#41](https://github.com/vertical-cloud-lab/byu-vcl/issues/41#issuecomment-4284403253),
  which has the contact. Ask them to quote the 9296SS-250-580 or an equivalent: a two-stage
  regulator with a CGA 580 inlet that reaches at least 150 psi and has a stainless diaphragm.
  Whoever orders the lab's argon may be able to add it to a gas order.

## eBay

Searched on 28 Oct 2026 from the lab Pi (see [How the search was done](#how-the-search-was-done)).
"harris 9296" returned 46 listings. Searches for the part numbers 9296-250-580 and 3302609 found
no exact matches, only other regulators.

**The one 250 psi argon unit:**

| Listing | Price | Condition | Returns | Seller |
| --- | --- | --- | --- | --- |
| [Harris 9296, 250 psig delivery, Ar/He/N2](https://www.ebay.com/itm/267822452773) | $175 + freight | Used. Comes with an outlet extension and a Parker Super-Lok shutoff valve | None | Lenmark Industries, Canada, 95.4 % positive (1,134) |

**125 and 150 psi argon units.** All of these have a 0–150 psi delivery gauge or a 125 or 150 psi
label, so they would run at 77–93 % of their range at 116 psi:

| Listing | Price | Condition | Returns | Seller |
| --- | --- | --- | --- | --- |
| [9296SS, CGA 580](https://www.ebay.com/itm/257791199091) (also a [second unit](https://www.ebay.com/itm/257791114230)) | $59.95 + $10 | Used. Label reads 125 psi, but a 0–4000 psi gauge is fitted to the delivery port, so it needs a new gauge | 30 days, buyer pays; seller's 30-day warranty | centratech, San Diego, 99.9 % (1.6K) |
| [9296SS, Ar/He/N2](https://www.ebay.com/itm/388146108758) | $95 + $18.33 | Used. 0–150 psi gauge; a flow valve and hose barb are fitted to the outlet | 30 days, buyer pays | \*\*labby\*\*, North Carolina, 100 % (96) |
| ["New old stock" 9296, Ar/He/N2, 150 psig](https://www.ebay.com/itm/204942452521) | $124.99, free shipping | Open box. 0–150 psi gauge; old thread sealant on the outlet nipple suggests it has been installed before | 30 days, seller pays | Plourde's Tool Box Bargains, 99.9 % (20K) |
| [9296SS, CGA 580, 0–125 psi](https://www.ebay.com/itm/405399856199) | $165 + $8.95 | Used | Not checked | industrialwelding-dot-net, 99.8 % (12.4K) |
| [9296SS-125-580](https://www.ebay.com/itm/405074061977) | $250 | Used | Not checked | next.day.automation, 99.9 % (49.9K) |
| [9296-125-580](https://www.ebay.com/itm/326799921260) | $349.99 + $7.10 | New | Not checked | jerry194, 99.3 % (3.4K) |

**The rest.** Most of the other listings were 9296s for CO2, hydrogen or methane, oxygen or fuel
gas, or 50 psi versions. One [Ar/He/N2 9296](https://www.ebay.com/itm/198520364291) at $450, used
and with no returns, didn't give its range. The non-Harris CGA 580 regulators were mostly
single-stage nitrogen purge regulators (TurboTorch and Radnor GP250 and TPR250, Harris 25GX). One
Victor VTS250C two-stage inert-gas regulator was $99 used, but its delivery range wasn't checked.

**Verdict.** The Lenmark unit would save about $340–$380 against a new one, before freight and
any import fees. But it can't be returned, it comes from Canada, and its history is unknown. The
125 psi units are cheaper still, but they'd run at the top of their range, and most need outlet
adapters or a new gauge. For a regulator on a 5N argon line, buy new.

## Outlet fitting

- **What to buy:** a straight connector, 1/4" NPT male × **6 mm** push-to-connect, rated for
  at least 150 psi. One example is Tameson's
  [F25TN](https://tameson.com/products/f25tn-6mm-x-1-4inch-npt-plug-in-fitting-with-male-threads-brass-pa-66-nbr-2-pieces),
  which has a brass thread, a PA 66 body and NBR seals.
- **Don't use a 1/4" tube fitting.** The machine's tube is metric 6/4 mm, and a 1/4" (6.35 mm)
  fitting won't grip 6 mm tube reliably.
- **Fitting it:** seal the NPT thread with PTFE tape or paste unless it comes pre-coated. Keep
  tape off the first thread so shreds can't get into the regulator. Leak-check with Snoop at
  8 bar.
- **Before returning the borrowed regulator:** check whose push fitting is in its outlet now.
  On the 17 Sept call, the push fittings for the compressed air were to come from BYU's side, so
  this one may be ours as well. If it is, move it to the new regulator.

## The Amazon regulator

**Still to do: send it back.** The order email is being forwarded so the return can be started
(20 Oct comment on #163). Nothing in this repo or in byu-vcl records which regulator it was or
what was wrong with it. The only trace is a 26 Sept comment on
[byu-vcl#232](https://github.com/vertical-cloud-lab/byu-vcl/pull/232#issuecomment-5845793220)
asking whether "that regulator came in yet".

Amazon's usual return window is 30 days from delivery. If the regulator arrived in late
September, that window has probably closed. Once the email turns up:

1. **Try the normal return first.** Open the order under *Your Orders*. If *Return or replace
   items* is still there, use it, giving defective or not as described as the reason.
2. **If a third-party seller sold it,** message the seller. If that doesn't resolve it, file an
   A-to-z Guarantee claim. That route is reported to stay open for 90 days after the latest
   estimated delivery date, after giving the seller 48 hours to respond. Check Amazon's A-to-z
   help page for the current terms.
3. **If Amazon sold it,** contact Amazon customer service and explain that it arrived defective.
4. **Record it here.** Add the listing, seller, price and what was wrong, so it doesn't get bought
   again.

Most Amazon "argon regulators" are welding flowmeter regulators. These are preset to about 50 psi,
and only the flow can be adjusted, often to no more than about 60 SCFH (for example the Flame Tech
[100-FL-AR-60-580](https://store.cyberweld.com/products/flame-tech-argon-flowmeter-regulator-100-fl-ar-60-580)).
That is the kind AMAZEMET's engineer warned against.

## How the search was done

The searches ran on the atomizer panel Pi (`tag:rpi-5-3ray`), so the sites saw an ordinary
desktop browser on the lab network rather than a cloud runner. The Pi runs a headed Chromium on
its desktop, with DevTools bound to its own `127.0.0.1:9222`. The session reached it through an
SSH tunnel and drove it with [`scripts/pi_browser.py`](scripts/pi_browser.py). That script sends
only input events: mouse moves along eased curves, clicks, per-key typing and wheel scrolls.

- **Playwright got blocked.** Attached with `connect_over_cdp`, Playwright got eBay's "Something
  went wrong on our end" page on the first search. A bare DevTools client that never calls
  `Runtime.enable` got through.
- **Zoro blocked both** ("Access is temporarily restricted").
- **1 GB of RAM is tight.** eBay item pages with their photos pushed the Pi into swap and crashed
  Chromium once. The script now blocks images, fonts and video in its tab, and listing photos were
  downloaded from `i.ebayimg.com` on the runner instead.
- **eBay sometimes refuses item pages.** It served its error page once, on a repeat visit to a
  listing that had loaded earlier.
