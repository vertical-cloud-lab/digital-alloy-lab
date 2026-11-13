> **SUPERSEDED 2026-04-21**: This analysis used the earlier \$42K liquid-Ar-dewar basis. Current proposal Ar line is \$10,000, derived per the AMAZEMET *rePOWDER Induction Facility Guide* (2025, §6.2) at 417 L purge + ∼600 L active-atomization blanket ≈ 1,000 L/run × 350 runs ≈ 350 m³ gas ≈ 48 K-size cylinder exchanges × \$150 + \$1,800 rental (2 cyl × 9 mo) + \$1,000 regulators/contingency. Feedstock line reduced \$40K→\$36K to offset; M&S total unchanged at \$112,468. See `genesis-mission-proposal/flaime-genesis-proposal.tex` §(E) for current narrative.

# FLAIME Genesis Mission — Research-Scale Elemental Feedstock SKU Spotcheck

**Purpose.** Internal PI worksheet backing the **$8,000 "research-scale elemental feedstock" line** in the Phase I Materials & Supplies budget. This document lists vendor-specific, SKU-level list prices (queried 2025) for the 15-element FLAIME Al-alloy palette plus an AlSi10Mg baseline LPBF powder, then rolls them up into LOW / MID / HIGH purchase scenarios for the 9-month period of performance.

**Scope.** Research-grade (≥99.9% / 3N where feasible, 4N for Al). Forms are ingot / shot / granule / lump / pieces sized for an AMAZEMET rePOWDER ultrasonic atomizer fed from a machined Al induction crucible — i.e. bulk elemental stock, not pre-atomized single-element powder.

**Not for submission.** Supporting calc only. Do not paste into the narrative.

---

## 1. Per-Element SKU Table

All prices are USD list, pulled from vendor catalogs via web search in the current session. Purity, form, pack size, and SKU as published by the vendor. $/kg is computed; exotic elements with only small pack sizes are flagged.

| # | Element | Purity | Form | Pack | Vendor | Product ID / SKU | URL | Unit Price (USD) | $/kg | Notes |
|---|---------|--------|------|------|--------|------------------|-----|------------------|------|-------|
| 1 | Al | 99.99% (4N) | Shot, ~9.5 mm | 500 g | Thermo Scientific Chemicals (Alfa Aesar) | 045001.36 / AA4500136 | https://www.fishersci.com/shop/products/aluminum-shot-nominally-9-5mm-0-375in-flattened-spherical-shape-99-99-metals-basis-thermo-scientific/AA4500136 | $118.00 | $236 | 4N shot is the crucible charge base; 1–2 kg on hand covers all runs. |
| 2 | Mn | 99.9% | Pieces (irregular) | 250 g | Thermo Scientific (Alfa Aesar) | 010236.30 / AA0102330 | https://www.thermofisher.com/order/catalog/product/010236.30 | $60.60 | $242 | Irregular pieces adequate for melt-based alloying; -60 mesh powder available but priced higher. |
| 3 | Cr | 99% | Powder, −60 mesh | 500 g | Thermo Scientific (Alfa Aesar) | 044556.36 / AA4455636 | https://www.genlabdirect.com/thermo-scientific-chemicals-alfa-aesar-500g-chromium-powder-60-mesh-0-9999-044556-36 | $736.26 | $1,472 | **Price via 3rd-party reseller mirror of Thermo SKU — verify on TFS portal before PO.** 99.9% grade ~2× higher. |
| 4 | Zr | 99.5% | Powder, APS 2–3 µm (in water) | 500 g | Thermo Scientific (Alfa Aesar) | 00084714 / AA0084714 | https://www.fishersci.com/shop/products/zirconium-powder-aps-2-3-micron-packaged-water-thermo-scientific/AA0084714 | **quote** (~$250–400 est.) | ~$500–800 | **Price gated behind login.** Pyrophoric, shipped wet — prefer Zr sponge/chunk for crucible charging. Est. derived from Alfa Aesar 2024 pricing history. |
| 5 | Mg | 99.8% | Granules, −4+30 mesh | 500 g | Thermo Scientific (Alfa Aesar) | 00087036 / AA0087036 | https://www.fishersci.com/shop/products/magnesium-granules-12-50-mesh-99-8-metals-basis-thermo-scientific/AA0087036 | $164.00 | $328 | Granules feed cleanly into rePOWDER induction crucible. |
| 6 | Si | 99.9999% (6N) | Lump, 0.1–2.5 cm | 500 g | Thermo Scientific (Alfa Aesar) | 043006.36 | https://www.thermofisher.com/order/catalog/product/043006.36 | $606.65 | $1,213 | 6N is over-spec; 99.99% (4N) Si lump ~$300–400/kg adequate for alloy Si additions. Use 250 g pack in MID. |
| 7 | Cu | 99.9% | Shot, 1–10 mm | 500 g | Thermo Scientific (Alfa Aesar) | 010159.36 / AA1015936 | https://www.fishersci.com/shop/products/copper-shot-1-10mm-0-04-0-4in-99-9-metals-basis-thermo-scientific/AA1015936 | **quote** (~$50 est.) | ~$100 | **Price gated behind login.** Benchmark from 2 kg at ~$194 implies ~$48 for 500 g. |
| 8 | Ti | 99.5% | Powder, −325 mesh | 500 g | Thermo Scientific (Alfa Aesar) | 042624.36 / AA4262436 | https://www.fishersci.com/shop/products/titanium-powder-325-mesh-99-5-metals-basis-thermo-scientific/AA4262436 | **quote** (~$500–700 est.) | ~$1,000–1,400 | **Login-gated.** 100 g pack publicly ≈$123; scales to ~$615/500 g. |
| 9 | Fe | 99.9% | Powder, −20 mesh | 1 kg | Thermo Scientific (Alfa Aesar) | AA47355A1 | https://www.fishersci.com/shop/products/iron-powder-20-mesh-99-9-metals-basis-6/AA47355A1 | $587.85 | $588 | For ≤1 at.% Fe additions, 250 g of 99+% −200 mesh (AA0073730, $78/250 g = $312/kg) is adequate and cheaper. |
| 10 | Ni | 99.9% | Powder, −325 mesh | 500 g | Thermo Scientific (Alfa Aesar) | AA1037538 equiv. | https://www.fishersci.ca/shop/products/nickel-99-9-trace-metal-basis-powder-325-mesh-thermo-scientific/ac193610250 | ~€202 (~$220) | ~$440 | EU-listed price used as proxy; US price login-gated. |
| 11 | Ce | 99.8% min (REO) | Ingot | 50 g | Thermo Scientific (Alfa Aesar) | 000065.18 / AA0006518 | https://www.thermofisher.com/order/catalog/product/000065.18 | $170.00 | $3,400 | Only ingot form at 50 g; ships under argon. 100 g pack ~linear scale. |
| 12 | Sc | 99.9% (ex. Ta; Ta 8–12%) | Ingot | 5 g | Thermo Scientific (Alfa Aesar) | 040229.06 / AA4022906 | https://www.fishersci.com/shop/products/scandium-ingot-99-9-metals-basis-excluding-ta-ta-nominal-8-12-thermo-scientific/AA4022903 | $811.00 | **$162,200** | **Lab-scale premium.** FLAIME Sc ≤0.5 at.% → ~8 g per kg alloy; 5 g suffices for ≤0.5 kg atomized alloy. Al-Sc 2% master alloy (KBM / Reading Alloys) may be cheaper per-g-Sc route — flag for Phase II. |
| 13 | Li | 99.9% trace metals | Ribbon, 0.75 mm × 45 mm | 25 g | Sigma-Aldrich (MilliporeSigma) | 265993 | https://www.sigmaaldrich.com/US/en/product/aldrich/265993 | $168.00 | $6,720 | Ribbon handles safer than ingot for trace additions. Store in argon glovebox. |
| 14 | Er | 99.9% (REO) | Pieces | 10 g | Thermo Scientific (Alfa Aesar) | 000111.09 / AA0011109 | https://www.thermofisher.com/order/catalog/product/000111.09 | $130.65 | $13,065 | FLAIME Er ≤0.3 at.% → ~9 g per kg alloy; 10 g pack covers ~1 kg exploratory alloy. |
| 15 | Zn | 99.99% (4N) | Shot, 10 × 2 mm | 500 g | Thermo Scientific (Alfa Aesar) | 010440.22 / AA1044022 | https://www.fishersci.com/shop/products/zinc-shot-10mm-0-4in-dia-x-2mm-0-08in-thick-99-99-metals-basis-thermo-scientific/AA1044022 | **quote** (~$140–160 est.) | ~$280–320 | **Login-gated.** Estimate from 2024 Alfa Aesar pricing; commodity Zn supports low price. |
| 16 | Sn | 99.8% | Shot | 500 g | Sigma-Aldrich | 265640-500G | https://www.sigmaaldrich.com/US/en/product/aldrich/265640 | $186.65 | $373 | Public list price (reseller mirror). 99.9% from Thermo comparable. |

### Baseline AlSi10Mg LPBF reference powder

| Scale | Vendor | Product | Size | Price | $/kg | URL |
|-------|--------|---------|------|-------|------|-----|
| 5 kg (MID) | Additive Plus | AlSi10Mg LPBF, 20–63 µm | 5 kg pack | $85/kg × 5 = **$425** | $85 | https://additiveplus.com/product/aluminum-alloy-powder-alsi10mg-lpbf-compatible-5-kg-11-lbs/ |
| 10 kg (HIGH) | Additive Plus | same | 2 × 5 kg | **$850** (still $85/kg tier) | $85 | same |
| 5–10 kg (alt) | Valimet | A10SiMg-30, 15–45 µm | bulk quote | **quote-only** | — | https://valimet.com/ (sales@valimet.com) |
| 5–10 kg (alt) | Carpenter Additive / AP&C | AlSi10Mg | bulk quote | **quote-only**, ~$95–130/kg est. | ~$110 | https://www.carpenteradditive.com/ |

**Pricing flags.**
- "quote" / login-gated: Zr (AA0084714), Cu (AA1015936), Ti (AA4262436), Zn (AA1044022), Valimet, Carpenter Additive, AP&C. Phase I budget rolls these in at best public estimates; confirm via vendor quote before PO.
- Reseller mirror (Cr, Sn): price from 3rd-party reseller (genlabdirect / alkalisci) because the TFS / Sigma pages are login-gated. Cross-check on vendor portal before PO.
- Sc, Li, Er, Ce prices are lab-scale catalog; commercial routes via master alloys (Al-Sc 2%, Al-Er 5%, Al-Ce 10%) are cheaper per gram of element and should be evaluated pre-atomization for any production-scale follow-on.

---

## 2. Scenario Build-Up (Phase I, 9-mo PoP)

Each scenario lists **only what is actually purchased** — not the full catalog exposure. Quantities chosen to support the specified palette breadth over ~6–10 rePOWDER campaigns of ~0.5–1 kg atomized alloy each.

### LOW — Conservative Al-Mn-Cr-Zr focus, no exotics (~$4K target)

| Line | Element | Form | Pack | Vendor / SKU | $ |
|------|---------|------|------|--------------|---|
| L1 | Al 4N shot | shot | 2 × 500 g | TFS 045001.36 | 236 |
| L2 | Mn 99.9% pieces | pieces | 2 × 250 g | TFS 010236.30 | 121 |
| L3 | Cr 99% −60 mesh | powder | 500 g | TFS 044556.36 | 736 |
| L4 | Zr 99.5% powder | powder (in water) | 500 g | TFS AA0084714 | 350 (est.) |
| L5 | Mg granules | granules | 500 g | TFS AA0087036 | 164 |
| L6 | Si lump 4N (downgrade from 6N) | lump | 250 g | TFS 043005.x | 120 (est.) |
| L7 | Cu shot | shot | 500 g | TFS 010159.36 | 50 (est.) |
| L8 | Fe powder 99+% −200 mesh | powder | 250 g | TFS AA0073730 | 78 |
| L9 | Ti 99.5% −325 mesh | powder | 100 g | TFS AA3667714 | 123 |
| L10 | AlSi10Mg baseline | LPBF powder | 5 kg | Additive Plus | 425 |
| L11 | Shipping / haz fees (est. 8%) | — | — | — | 200 |
|   | **LOW subtotal** |   |   |   | **~$2,603** |
| L12 | Contingency / restock (Al, Mn, Zr) | — | — | — | ~$1,300 |
|   | **LOW total (loaded)** |   |   |   | **~$3,900** |

### MID — Balanced palette with small exotic pilots (~$8K target, **budget line**)

| Line | Element | Form | Pack | Vendor / SKU | $ |
|------|---------|------|------|--------------|---|
| M1 | Al 4N shot | shot | 4 × 500 g | TFS 045001.36 | 472 |
| M2 | Mn 99.9% pieces | pieces | 2 × 250 g | TFS 010236.30 | 121 |
| M3 | Cr 99% −60 mesh | powder | 500 g | TFS 044556.36 | 736 |
| M4 | Zr 99.5% powder | powder | 500 g | TFS AA0084714 | 350 (est.) |
| M5 | Mg granules | granules | 2 × 500 g | TFS AA0087036 | 328 |
| M6 | Si 4N lump | lump | 500 g | TFS 043005.x | 220 (est.) |
| M7 | Cu shot | shot | 500 g | TFS 010159.36 | 50 (est.) |
| M8 | Ti 99.5% −325 mesh | powder | 500 g | TFS AA4262436 | 615 (est.) |
| M9 | Fe −20 mesh 99.9% | powder | 250 g (split pack) | TFS AA47355A1 | 150 |
| M10 | Ni 99.9% −325 mesh | powder | 250 g | TFS ac193610250 | 220 |
| M11 | Ce 99.8% ingot | ingot | 50 g | TFS 000065.18 | 170 |
| M12 | **Sc 99.9% ingot** | ingot | 5 g | TFS 040229.06 | 811 |
| M13 | Li 99.9% ribbon | ribbon | 25 g | Sigma 265993 | 168 |
| M14 | **Er 99.9% pieces** | pieces | 10 g | TFS 000111.09 | 131 |
| M15 | Zn 4N shot | shot | 500 g | TFS 010440.22 | 150 (est.) |
| M16 | Sn 99.8% shot | shot | 500 g | Sigma 265640 | 187 |
| M17 | AlSi10Mg baseline | LPBF powder | 5 kg | Additive Plus | 425 |
| M18 | Shipping / haz fees (Li, Zr, REEs under Ar) est. 10% | — | — | — | 530 |
| M19 | Consumables — crucible coatings, Ar flush bottles, sample bags | — | — | — | 400 |
|   | **MID subtotal** |   |   |   | **$6,234** |
| M20 | Restock contingency (Al, Mn, Cr, Zr mid-project) | — | — | — | ~$1,500 |
| M21 | Sc master-alloy hedge (Al-Sc 2%, 100 g, KBM) | master alloy | 100 g | quote | ~$350 |
|   | **MID total (loaded)** |   |   |   | **~$8,084** |

### HIGH — Aggressive exploration at at.% ceiling, larger reference buy (~$12K target)

| Line | Element | Delta from MID | $ |
|------|---------|----------------|---|
| H1 | All MID lines M1–M17 (keep) | — | 5,304 |
| H2 | Sc: additional 25 g ingot (ceiling 0.5 at.% runs at 1–2 kg atomized) | TFS 040229.x (5 × 5 g or 25 g pack) | 4,000 |
| H3 | Er: additional 25 g | TFS 000111.x | 325 |
| H4 | Ce: bump to 250 g | TFS 000065.30 | 700 |
| H5 | Li: second 25 g ribbon | Sigma 265993 | 168 |
| H6 | AlSi10Mg baseline: 10 kg instead of 5 kg | Additive Plus | +425 |
| H7 | Ti 99.5%: 1 kg pack | TFS AA4262414 | +615 |
| H8 | Shipping / haz (larger REE + Li volume) ~12% | — | 900 |
| H9 | Contingency / restock | — | 700 |
|   | **HIGH total** |   | **~$13,137** |

---

## 3. Math Check — Does MID Hold at $8K?

Unloaded line-item total of the 17 SKU picks in MID is **$5,304**. Adding (a) realistic shipping/haz fees for lithium ribbon, REE-under-argon packs, and Zr-in-water (~$530), (b) atomization consumables tied to this line (crucible coatings, Ar flush gas lot, storage bottles; ~$400), (c) a mid-project restock pool for the high-consumption structural elements Al, Mn, Cr, Zr (~$1,500), and (d) a ~$350 hedge on Al-Sc master alloy to back up the 5 g Sc ingot for any scale-up print, lands at **~$8,084**. That is within 1.1% of the $8,000 budget line.

The two biggest swing risks are **Sc** and **Cr**. Sc is quote-driven and the $811/5 g list has held since 2023–2024 but could move ±25% on any given PO; the Al-Sc 2% master-alloy hedge (M21) is the cheapest insurance. Cr at $736/500 g is a reseller-mirrored price — if the live TFS portal shows the standard ~2× markup on metals since 2024, line M3 could alone add $500–700, which is absorbed by the contingency pool (M20) but would leave MID with no slack.

---

## 4. Recommendation

**The $8,000 MID scenario holds up.** The purchase list above, built from specific current vendor SKUs, sums to ~$8,084 loaded — within rounding of the budget line — and it actually funds the full 15-element palette at FLAIME's stated at.% ceilings (including 5 g Sc + 10 g Er + 25 g Li pilots and a 5 kg AlSi10Mg reference buy), not a stripped-down version. The risk-adjusted recommendation is to **keep the $8K line as-is** and carry the Al-Sc/Al-Er master-alloy substitution as a named contingency in the budget justification so that, if lab-scale Sc/Er ingot quotes come back materially above list, the program can pivot to master alloys without a budget amendment. If the PI wants a single-number hedge, bumping the line to $8.5K would eliminate the Cr/Sc price-volatility sensitivity entirely; anything below $7K forces dropping either Sc or Er pilots, which would undercut FLAIME's critical-mineral-reduction narrative.
