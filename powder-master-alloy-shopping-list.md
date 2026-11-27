# Powder & Master-Alloy Shopping List

Procurement reference for elemental powders, master alloys, and pre-alloyed
feedstocks needed to feed the FLAIME (Fast Learning AI for Mineral Efficiency)
Phase I powder-to-tensile pipeline (Genesis Mission, DOE DE-FOA-0003612,
Topic 3B). Scope is set by the canonical 15-element Al-based palette defined
in [`genesis-mission-proposal/flaime-genesis-proposal.tex`](genesis-mission-proposal/flaime-genesis-proposal.tex)
(line 171):

> `\elementpalette = Mn, Cr, Zr, Mg, Si, Cu, Ti, Fe, Ni, Ce, Sc, Li, Er, Zn, Sn`

Always-present base: **Al**. Together: 16 elements covering 22,803 ternary
through 9-component sub-systems. Initial focus: **Al–Mn–Cr–Zr** and **Al–Zr**.

Companion documents:

- [`company-landscape.md`](company-landscape.md) — strategic vendor profiles & Genesis Mission partnership ratings
- [`alloy-workflow-review.md`](alloy-workflow-review.md) — pipeline status, in-lab feedstocks, autotrickler/flow notes
- [`alloy-databases.md`](alloy-databases.md) — composition/property database context
- Powder-doser hardware: [vertical-cloud-lab/powder-doser#19](https://github.com/vertical-cloud-lab/powder-doser/pull/19)

> **Pricing notice.** All prices in this document are **indicative USD as of
> 2026-Q2** for *research / R&D quantities* (≤1 kg lots) and are intended for
> budgeting only. Actual cost depends heavily on purity, particle-size
> distribution (PSD), morphology, lot size, packaging (Ar-purged vs. air),
> shipping (DG fees apply for Mg, Li, fine Al, Zr, Ti), and incoterms. Always
> obtain a written quote before committing budget. Rare-earth and Sc spot
> prices (Treibacher, MP Materials, Lynas indices) move materially quarter
> over quarter. Where commodity grade is irrelevant (Cu, Fe, Ni, Zn, Sn, Mg,
> Al), 100 g–1 kg research-grade pricing is dominated by packaging and
> handling rather than commodity value.

> **Powder-only procurement preference.** Per PI direction (PR review,
> 2026-05), **every feedstock on this list must arrive in powder form** so it
> can drop directly into the autotrickler / rePOWDER pipeline without an
> intermediate ingot-machining or re-melt step at BYU. Per PI direction
> (PR review, 2026-06) we are **not** planning to rely on Valimet
> toll-atomization for most feedstocks; the Phase I default is **off-the-shelf
> catalog powder from scientific / research-grade suppliers** — primarily
> [American Elements](https://www.americanelements.com/) and
> [Stanford Advanced Materials](https://www.samaterials.com/) (plus Goodfellow,
> Sigma-Aldrich, Thermo Fisher / Alfa Aesar, Micron Metals, Heeger). The
> procurement path, in priority order, is: **(a) buy the element or Al-X
> alloy as an off-the-shelf catalog powder** from a scientific supplier
> (Ar-packed for pyrophoric Sc, Zr, Ti; water-wet or coarse-PSD for Mg);
> **(b) ask an AM-powder producer for a custom *atomized* SKU** (Sandvik
> Osprey, Carpenter Additive, AP&C, Tekna, Equispheres, Elementum 3D produce
> custom Al-X master-alloy powders on quote) when no catalog powder exists at
> the needed PSD; **(c) only as a last resort**, place an ingot order with
> Valimet (funded partner) for toll-atomization to 15–63 µm
> spherical powder (adds ~2–4 weeks).
>
> **What these powders feed (PI direction, 2026-06).** The off-the-shelf
> elemental and master-alloy powders bought via (a)/(b) are the **feedstock
> dosed into the high-purity Al crucible and ultrasonically atomized in-house
> on the AMAZEMET rePOWDER** (induction crucible module). Getting these
> **in-house ultrasonic atomization runs going in smaller quantities is the
> immediate procurement goal** — it is the proposal's primary
> composition-iteration route (see proposal lines 849–854). The larger
> **gas-atomization scale-up collaboration with Valimet is worth pursuing in
> parallel** for a subset of production-scale lots, but it is **not** what we
> are procuring for first; the immediate buys are sized to seed small in-house
> ultrasonic atomization runs.
>
> **Startup-fund budget cap (PI direction, 2026-06).** The *immediate*
> precursor spend is capped at **~$2–5K from startup funds** — this is **not**
> the full Phase I award M&S budget. The shopping list below is therefore
> written in two tiers: a **Round-1 startup-fund bundle (~$2–5K, §0 / §4.A)**
> sized only to *get a handful of initial in-house ultrasonic atomization runs
> going* on the Al–Mn–Cr–Zr / Al–Zr focus systems, and the **full Phase I
> award-scope reference (~$24K, §4.B)** kept for context once the DOE award
> M&S budget is available. The AMAZEMET rePOWDER atomizes from a **minimum
> ~50 g feedstock charge per run** (≥80% yield to in-PSD powder; see
> [AMAZEMET R&D atomization service](https://www.amazemet.com/amazemet-new-business-line-atomization-service/)),
> so a few hundred grams of each precursor covers many composition-iteration
> runs — the startup-fund bundle buys research-quantity (50–500 g) lots, not
> kilograms.

---

## 0. First Things to Order (TL;DR) — $2–5K startup-fund bundle

**Budget context (PI direction, 2026-06): the immediate precursor spend is
~$2–5K from startup funds**, not the full Phase I award. The goal of this
first PO round is narrow: **buy just enough off-the-shelf research-quantity
powder to get a handful of in-house ultrasonic atomization runs going** on the
Al–Mn–Cr–Zr and Al–Zr initial focus systems. Because the AMAZEMET rePOWDER
atomizes from a **~50 g minimum feedstock charge per run** (≥80% yield), a few
hundred grams of each precursor is enough for many composition-iteration runs —
so this round buys **50–500 g lots, not kilograms**. Every line is an
off-the-shelf catalog powder from a scientific / research-grade supplier; we
are *not* routing these through Valimet toll-atomization (PI direction,
2026-06).

**Minimum viable bundle (~$1.5–2.5K) — enough to start atomizing Al–Mn–Cr–Zr / Al–Zr:**

1. **High-purity Al 1199-equivalent (99.99%, 4N) powder, ≤45 µm, 500 g** — off-the-shelf [American Elements 4N/5N Al powder](https://www.americanelements.com/aluminum-powder-7429-90-5) (~$120–250/100 g → ~$700–1,000/500 g) is the controlled-composition matrix baseline; 99.99% keeps Fe/Si/Cu impurities out of the alloy chemistry. Backup: [Stanford Advanced Materials AM-grade Al powder](https://powder.samaterials.com/aluminum.html). This is the dominant mass in every melt; 500 g seeds ~10 runs at 50 g.
2. **Electrolytic Mn powder, 99.9%, –100/+325 mesh (45–150 µm), 100 g** from [American Elements](https://www.americanelements.com/manganese-powder-7439-96-5) (~$80–150). Backups: [Stanford Advanced Materials Mn powder](https://www.samaterials.com/micro-nano-materials/256-micro-manganese-powder.html); [Alfa Aesar / Thermo Fisher](https://www.thermofisher.com/order/catalog/product/036350) Mn powder.
3. **Cr powder, 99.5%, 45–75 µm (coarsest available), 100 g** from [American Elements](https://www.americanelements.com/chromium-powder-7440-47-3) or [Stanford Advanced Materials](https://www.samaterials.com/chromium/1313-chromium-metal-powder-cr-powder.html) (~$75–160). Cr flows poorly at <45 µm — request the coarsest spheroidized SKU available. Backup: [Micron Metals (AEE)](https://micronmetals.com/) Cr-101/102.
4. **Zr powder, water-wet, 99.5%, ≤45 µm, 100 g** from [American Elements](https://www.americanelements.com/zirconium-powder-7440-67-7) (~$250–450, **DG class 4.2**, ships water-wet — add ~$100–300 hazmat). Backup elemental: [Goodfellow](https://www.goodfellow.com/usa/) Ar-packed Zr powder. (Master-alloy / toll-atomization fallback only if DG handling blocks; off-the-shelf elemental Zr is the default.)
5. **Coarse Si powder, 99.5%, 45–106 µm, 250 g** from [Heeger Materials 45–106 µm spherical Si](https://heegermaterials.com/silicon-powders/74-45-106-micron-spherical-silicon-si-powder.html) or [Micron Metals (AEE)](https://micronmetals.com/) (~$150–300). Direct powder fix for the autotrickler gumming issue documented in [`alloy-workflow-review.md` §1.5](alloy-workflow-review.md) and [powder-doser#19](https://github.com/vertical-cloud-lab/powder-doser/pull/19). Backups: [American Elements Si powder](https://www.americanelements.com/silicon-powder-7440-21-3); [Stanford Advanced Materials Si powder](https://www.samaterials.com/silicon/1060-silicon-powder.html).

That core five lands around **~$1.5–2.5K** including DG shipping and is enough
to start atomizing the Al–Mn–Cr–Zr / Al–Zr focus chemistries.

**Optional adds to use the rest of a ~$5K envelope (only if funds allow):**

6. **More Al matrix (+500 g, ~$700–1,000)** and/or **larger Mn/Cr/Zr lots (250 g each, +~$400)** to extend the number of runs before re-ordering.
7. **Al–2Sc master alloy as powder, ~50–100 g small lot** — [American Elements Sc–Al alloy](https://www.americanelements.com/scandium-aluminum-alloy-113413-85-7) or [Sigma-Aldrich 755672 Al–2Sc](https://www.sigmaaldrich.com/US/en/product/aldrich/755672) (note: Sigma is a ~1 g ingot at ~$420–595, so prefer a small American Elements / SAM powder lot, or a custom atomized SKU on quote). Sc is the highest-priced element in the palette; defer a larger Sc buy to the award-funded round unless a small validation lot is wanted now.
8. **Al–5Ti–1B master alloy as powder, ~100–250 g** — off-the-shelf or custom atomized SKU on quote from [Sandvik Osprey](https://www.metalpowder.sandvik/) / [Carpenter Additive](https://www.carpenteradditive.com/) / [AP&C](https://www.advancedpowders.com/) (~$200) for Ti grain refinement.

**Not part of the powder PO:** a **1199 Al billet** for the rePOWDER crucible /
dispense-vial stock ([McMaster-Carr](https://www.mcmaster.com/products/aluminum/),
[OnlineMetals](https://www.onlinemetals.com/en/buy/aluminum), ~$100–200 for a
small round) is bought separately as fixture stock, not as trickler feedstock —
use existing lab Al stock first if available.

**Round-1 startup-fund envelope:** **~$2–5K** (startup funds, *not* the Phase I
award M&S budget). Core five ≈ $1.5–2.5K; optional adds bring it toward $5K.
Defers Mg, Cu, Ti (beyond grain-refiner), Fe, Ni, Zn, Sn, Ce, Er, Li — and any
larger Sc buy — to the **award-funded Round 2** (full ~$24K scope in §4.B)
once first atomization runs and prints come back.

> **Why off-the-shelf powder over toll-atomization.** Waffle ingots
> are the cheapest unit-economics form ($25–80/kg alloy basis), but
> converting them to autotrickler-compatible powder via Valimet
> toll-atomization adds ~2–4 weeks of lead time — and per PI
> direction (2026-06) we are not planning to use Valimet for most feedstocks.
> Buying research-grade powder direct from American Elements / Stanford
> Advanced Materials (~$2–20/g depending on element) is faster, removes the
> ingot-handling step, and lets us **feed the AMAZEMET rePOWDER in-house
> ultrasonic atomizer in small quantities right away** — the immediate Phase I
> composition-iteration route (proposal lines 849–854). Valimet gas-atomization
> stays in view for a subset of production-scale lots, but it is a parallel
> scale-up track, not the immediate procurement focus.

---

## 1. Procurement Strategy at a Glance

The FLAIME pipeline doses mixtures of elemental (and master-alloy) powders into
high-purity Al crucibles at **0.1 mg dosing resolution** (typical 100 g batch),
then **ultrasonically atomizes the melt in-house via the AMAZEMET rePOWDER**
(with induction crucible module) into printable alloy powder. Getting these
in-house ultrasonic atomization runs going in smaller quantities is the
immediate goal these purchases serve; Valimet gas atomization is reserved for a
subset of production-scale lots (see proposal lines 849–854). Three procurement
classes follow:

| Class | What | Why | Typical PSD | Typical lot |
|---|---|---|---|---|
| **A. Bulk Al matrix** | High-purity Al for crucibles + balance | Largest mass fraction in every alloy; doubles as crucible/dispense vial | crucible billet (machined) + 15–63 µm AM powder | 1–5 kg per crucible billet; 5–25 kg powder lots |
| **B. Elemental alloying powders** | Mn, Cr, Si, Cu, Ti, Fe, Ni, Mg, Zn, Sn | Direct dosing for ternary–9-comp sub-systems | 20–75 µm where flowable; finer for low-add elements | 100 g–1 kg per element per year (Phase I) |
| **C. Master alloys (as powder)** | **Al–Sc, Al–Zr, Al–Mn, Al–Cr, Al–Er, Al–Ce, Al–Li** | Elements that are pyrophoric (Sc, Zr, Li), unflowable (Cr, Er), or rare-earth-cost-sensitive (Ce, Er, Sc) become safe/affordable when delivered as an Al-X master alloy — bought as off-the-shelf catalog powder where available, or a custom atomized SKU on quote | 15–63 µm powder (catalog or atomized SKU) | 0.5–2 kg powder lots |

**Why master alloys for the hard cases.** Elemental Cr powder passivates and
flows poorly; elemental Zr and Sc powders are pyrophoric and shipped under Ar;
elemental Li is air/water-reactive and ships only in mineral oil or sealed
ampoules; elemental Er and Ce are expensive at high purity. For these, an
Al-X master alloy is far safer and cheaper per gram of alloying element than
elemental research powder. Buy the master alloy as off-the-shelf catalog
powder where a scientific / AM supplier lists it; only fall back to a custom
atomized SKU on quote, or (last resort) an ingot toll-atomized by Valimet,
when no catalog powder exists at the needed PSD.

**Phase I priority order** (matches proposal Activity 2 + initial focus):

1. **Tier 1 (Al–Mn–Cr–Zr, Al–Zr starting Sep 2026):** high-purity Al matrix
   powder (American Elements 4N / Stanford Advanced Materials), elemental Mn,
   Cr, Zr powders (American Elements / SAM), elemental Si (coarse, Micron
   Metals).
2. **Tier 2 (next ~6 sub-systems):** Mg, Cu, Ti, Fe, Ni elemental powders + Al–2Sc master-alloy powder.
3. **Tier 3 (rare-earth and reactive expansion):** Ce, Er via Al–Ce / Al–Er master-alloy powder; Li via Al–Li; Zn and Sn elemental.

---

## 2. Element-by-Element Shopping List

For each element below: recommended physical form, suppliers (≥2), indicative
price, and notes. Links go to canonical product / category pages.

> **Vendor curation.** Suppliers in this list are deliberately limited to
> **scientific / research-grade and alloy-development houses**
> (American Elements, Sigma-Aldrich/Millipore Sigma, Alfa Aesar/Thermo Fisher,
> Goodfellow, MSE Supplies, Heeger Materials, Stanford Advanced Materials,
> EdgeTech Industries, Micron Metals / Atlantic Equipment Engineers,
> Treibacher) plus alloy-AM specialists
> (Valimet, AMAZEMET, Equispheres, Uniformity Labs, Carpenter Additive,
> Sandvik Osprey, AP&C, Tekna, Höganäs, Elementum 3D, Luxfer MEL,
> Indium Corp, Vale INCO, BASF carbonyl) and the standard master-alloy
> metallurgy houses (KBM Affilips, AMG Aluminum, Reading Alloys / Kymera,
> Arcadium Lithium). Pyrotechnic-, foundry-, and jewelry-supply vendors are
> intentionally excluded.
>
> **Note on link validation.** URLs were re-verified 2026-06. The
> **Stanford Advanced Materials** product-page deep links added in this
> revision (Cr `CR1313`, Si `1060`, Mn `MP0256`, Si/Sc category pages) were
> confirmed to resolve. A few SAM SKUs (the Sc metal-powder `1018` and
> Sc–Al alloy `1019` pages, and some Zr powder pages) load but are marked
> *Discontinued* — for those, request the current equivalent via the SAM
> element category page or buy the elemental powder from American Elements.
> **americanelements.com** continues to return HTTP 403 to headless tools
> (`curl`, Playwright) — it sits behind Cloudflare bot-protection requiring
> interactive JavaScript challenge solving — but opens normally in any human
> browser session, and the deep-link pattern (e.g.
> `americanelements.com/aluminum-powder-7429-90-5`) was confirmed valid by
> the PI. Höganäs, Onlinemetals, Arcadium Lithium, and GKN serve the same
> 403 pattern; sigmaaldrich.com and uniformitylabs.com return connection
> errors from headless probes but load normally interactively. Treat
> 403 / connection-refused-from-headless ≠ broken.

### 2.1 Aluminum (Al) — base + crucible + balance

| Form | Supplier | Product / page | Indicative price | Notes |
|---|---|---|---|---|
| **High-purity Al powder, 99.99% (4N), ≤45 µm (1199-equivalent)** | **[American Elements](https://www.americanelements.com/aluminum-powder-7429-90-5)** | Al powder, 4N/5N grades | $2–$8/g (100 g–1 kg) | **Preferred high-purity baseline** (per PI direction). Off-the-shelf scientific catalog 99.99–99.999% Al; keeps impurity elements (Fe, Si, Cu) out of the controlled-composition matrix without a toll-atomization step. |
| High-purity / AM-grade Al powder, spherical | [Stanford Advanced Materials](https://powder.samaterials.com/aluminum.html) | Al / Al-alloy AM powders | $2–$8/g | Off-the-shelf scientific co-primary; spherical AM-grade Al and Al-alloy powders. |
| Pure Al powder, 15–53 µm | [MSE Supplies](https://www.msesupplies.com/collections/mse-pro-aluminum-powder) (Tucson, AZ) | "Al powder, AM grade" | $120–$200/kg | Already a supplier of record (AlSi10Mg used in PoC, see `alloy-workflow-review.md` §1). |
| Pure Al gas-atomized powder, 15–45 µm | [Equispheres](https://www.equispheres.com/) (Ottawa, ON) | NExP-1 Al | $90–$150/kg | Ultra-narrow PSD; LPBF-optimized. |
| Al 1199 (99.99%) gas-atomized powder, 15–63 µm — **contingency only** | Valimet (Stockton, CA), toll-atomized from 1199 stock | [AM & cold-spray powders](https://valimet.com/additive-manufacturing-and-cold-spray-powders/) | quote | Funded partner. Held in reserve if off-the-shelf 4N powder cannot meet a needed PSD; not the default per PI direction (2026-06). S-grade (1100/Al-99.7) also available for bulk/non-critical matrix. |
| **Machined high-purity Al billet for crucible** | [McMaster-Carr](https://www.mcmaster.com/products/aluminum/) | 1199 / 1100 Al rod / round stock | $20–$60/lb | Supplier of record (PoC Al wire). **Use 1199 (99.99%)** for the high-purity crucible so it does not contaminate the controlled-composition melt; 1100 (99.0%) only for non-critical fixtures. |
| 1199 / 1100 Al wire (autotrickler feedstock) | [OnlineMetals](https://www.onlinemetals.com/en/buy/aluminum) | 1199 / 1100 Al wire | ~$20/lb | Supplier of record. |
| **AlSi10Mg pre-alloyed (PoC reference powder)** | MSE Supplies | [AlSi10Mg, 15–45 µm](https://www.msesupplies.com/collections/mse-pro-aluminum-powder) | ~$200–$300/kg | Already in lab; baseline for tensile/hardness comparison. |

**Recommendation.** Use **off-the-shelf high-purity Al 4N powder (1199-
equivalent)** from American Elements or Stanford Advanced Materials as the
controlled-composition matrix baseline. Machine 1199 Al billet for crucibles
to avoid contaminating the melt. Valimet toll-atomization from 1199 stock is a
contingency only (per PI direction), not the default. Hold MSE AlSi10Mg as a
calibration baseline.

---

### 2.2 Manganese (Mn)

Elemental Mn powder is electrolytic, brittle, and flows acceptably at
≥45 µm. Off-the-shelf elemental Mn powder from a scientific supplier is the
primary route; the Al–25Mn master alloy is a secondary option for repeatable
melt chemistry and to avoid Mn fume during atomization.

| Form | Supplier | Product / page | Indicative price | Notes |
|---|---|---|---|---|
| **Electrolytic Mn powder, 99.9%, –100/+325 mesh (45–150 µm)** | **[American Elements](https://www.americanelements.com/manganese-powder-7439-96-5)** | Mn powder | $2–$5/g (100 g pack) | **Recommended primary route** — off-the-shelf catalog powder; request coarsest grade for flow. |
| Mn powder, ≥99.5% | [Stanford Advanced Materials](https://www.samaterials.com/micro-nano-materials/256-micro-manganese-powder.html) | Mn powder (MP0256) | $2–$5/g | Off-the-shelf scientific co-primary. |
| Mn powder, 99.6%, ≤10 µm | [Alfa Aesar / Thermo Fisher](https://www.thermofisher.com/order/catalog/product/036350) | Catalog 036350 | ~$1–$3/g (100 g) | Coarser alternatives flow better in autotrickler. |
| Al–25Mn master alloy (waffle/ingot) | [KBM Affilips](https://www.kbmaffilips.com/) (Beerse, BE) | Aluminium master alloys | $25–$45/kg (alloy basis) | 10/15/20/25 wt% Mn grades; secondary option (request atomized SKU to keep powder form). |
| Al–25Mn master alloy | [AMG Aluminum](https://amg-al.com/) (Wayne, PA) | AMG Al-Mn master alloys | $25–$45/kg | US-based; equivalent to KBM. |

**Recommendation.** Buy off-the-shelf electrolytic Mn powder (American Elements
or Stanford Advanced Materials), coarsest grade available for flow. Keep an
Al–25Mn master alloy (as atomized powder) as a secondary route for high-Mn
melt practice.

---

### 2.3 Chromium (Cr)

Elemental Cr powder passivates rapidly (forms Cr₂O₃ skin), is brittle, and
**flows very poorly** through autotrickler-class equipment. Master-alloy
route is the **strongly recommended primary path**.

| Form | Supplier | Product / page | Indicative price | Notes |
|---|---|---|---|---|
| **Cr powder, 99.5%, coarsest grade (request ≥45 µm)** | **[American Elements](https://www.americanelements.com/chromium-powder-7440-47-3)** | Cr powder | $3–$8/g (100 g) | **Recommended primary** off-the-shelf route; request coarsest spheroidized SKU to mitigate flow problems. |
| Cr powder, 99.8–99.999% | [Stanford Advanced Materials](https://www.samaterials.com/chromium/1313-chromium-metal-powder-cr-powder.html) | Cr metal powder (CR1313) | $3–$8/g | Off-the-shelf scientific co-primary; spherical Cr grades also available. |
| Cr powder, 99.95%, ≤45 µm | [Micron Metals (AEE)](https://micronmetals.com/) | Cr-101 / Cr-102 | $4–$10/g (100 g) | Higher purity option. |
| Al–20Cr master alloy (as powder) | [KBM Affilips](https://www.kbmaffilips.com/) | Aluminium master alloys | $30–$60/kg (alloy basis) | 5/10/20 wt% Cr grades; secondary route (request atomized SKU) if elemental Cr flow is unworkable. |
| Al–20Cr master alloy | [AMG Aluminum](https://amg-al.com/) (Wayne, PA) | AMG Al-Cr | $30–$60/kg | US-based alloy-metallurgy house; equivalent to KBM. |

**Recommendation.** Buy off-the-shelf coarse Cr powder (American Elements or
Stanford Advanced Materials), coarsest grade available. If elemental Cr flow
proves unworkable, fall back to an Al–20Cr master alloy delivered as atomized
powder. Note Cr ≡ relevant supply-chain critical mineral for Genesis Mission
narrative — substitution-with-less-Cr is in scope.

---

### 2.4 Zirconium (Zr)

Elemental Zr powder is **pyrophoric** (UN 1358 Class 4.2 hazmat) and ships
only in Ar-purged or wet packaging — significant DG surcharge, restricted
courier. Off-the-shelf water-wet / Ar-packed Zr powder from a scientific
supplier is the default; an Al–Zr master alloy delivered as atomized powder is
the secondary route if DG handling proves a blocker (Al–Zr is a common
7000-series grain refiner).

| Form | Supplier | Product / page | Indicative price | Notes |
|---|---|---|---|---|
| **Zr powder, 99.5%, –325 mesh, water-wet** | **[American Elements](https://www.americanelements.com/zirconium-powder-7440-67-7)** | Zr powder | $8–$20/g (100 g) | **Recommended primary** off-the-shelf route; pyrophoric, ships water-wet (DG 4.2). |
| Zr powder, 99.9%, –325 mesh, Ar-packed | [Goodfellow](https://www.goodfellow.com/usa/) | Zr powder | $10–$25/g (100 g) | Scientific research catalog; passivated. |
| Al–10Zr master alloy (as powder) | [KBM Affilips](https://www.kbmaffilips.com/) | Aluminium master alloys | $35–$70/kg (alloy basis) | 5/10/15 wt% Zr grades; secondary route — request atomized SKU (no DG fees) if elemental Zr handling is a blocker. |
| Al–10Zr master alloy | [AMG Aluminum](https://amg-al.com/) | AMG Al-Zr | $35–$70/kg | US-based equivalent. |
| Al–10Zr master alloy | [Reading Alloys / Kymera International](https://www.kymerainternational.com/business-units/reading-alloys/) (Robesonia, PA) | Al master alloys | $35–$70/kg | US-based; specializes in Ti and Al master alloys. |

**Recommendation.** Off-the-shelf water-wet Zr powder from American Elements
(or Ar-packed from Goodfellow) is the primary feedstock for the Al–Zr and
Al–Mn–Cr–Zr focus systems. If DG handling becomes a blocker, fall back to an
Al–10Zr master alloy delivered as atomized powder.

---

### 2.5 Magnesium (Mg)

Mg metal powder is **flammable** (UN 1418 Class 4.3) and water-reactive in
fine form. Coarser PSD (≥75 µm) is safer to handle; master-alloy route also
viable but Mg vapor pressure during melt is the bigger constraint than
solid-state safety.

| Form | Supplier | Product / page | Indicative price | Notes |
|---|---|---|---|---|
| Mg powder, 99.8%, –50/+100 mesh (150–300 µm) | [Goodfellow](https://www.goodfellow.com/usa/) | Mg metal powder, coarse | $0.50–$2/g (1 kg) | Scientific catalog; coarse PSD safer and flowable. |
| Mg powder, 99.9%, –325 mesh | [American Elements](https://www.americanelements.com/magnesium-powder-7439-95-4) | Mg powder | $1–$3/g (100 g) | Fine; tighter SDS controls. |
| Mg powder, 99.8%, –20+100 mesh | [Sigma-Aldrich](https://www.sigmaaldrich.com/US/en/product/aldrich/254118) | 254118 (Mg turnings/powder) | $0.50–$2/g | Scientific research catalog. |
| Mg gas-atomized AM powder, 25–63 µm | [Luxfer MEL Technologies (Magnesium Elektron)](https://luxfermeltechnologies.com/) | SoluMag / Elektron® AM | quote only | OEM AM-grade Mg powder; produced primarily for biomedical AM. |
| **Al–10Mg master alloy** | KBM Affilips | [Aluminium master alloys](https://www.kbmaffilips.com/) | $20–$40/kg | Useful when Mg target ≤2 wt% (most Al alloys). |

**Recommendation.** Al–10Mg master alloy for routine additions ≤2 wt% (covers
most 5xxx/6xxx target chemistries); coarse Mg powder from Goodfellow for high-Mg
sub-systems. Atomization of fine Mg powder is fire-risk — do **not** add fine
Mg directly to the rePOWDER crucible without consulting AMAZEMET.

---

### 2.6 Silicon (Si)

Already in lab (McMaster, ~45 µm), but flow problems are documented in
[`alloy-workflow-review.md` §1.5](alloy-workflow-review.md) and the
[powder-doser PR #19](https://github.com/vertical-cloud-lab/powder-doser/pull/19).
Coarser, more spherical, AM-grade Si is recommended.

| Form | Supplier | Product / page | Indicative price | Notes |
|---|---|---|---|---|
| **Si powder, 99.5%, 45–106 µm (coarser, better flow)** | [Atlantic Equipment Engineers / Micron Metals](https://micronmetals.com/) | Si-103 / Si-104 | $0.50–$2/g (1 kg) | **Direct fix for autotrickler gumming.** |
| Si powder, 99.5%, –325 mesh (≤45 µm, fine) | McMaster-Carr | "silicon powder" | ~$50–$100 / lb | Current in-lab feedstock. Keep, but augment with coarser. |
| Si powder, 99.9–99.9999% (3N–6N), customizable PSD | [Stanford Advanced Materials](https://www.samaterials.com/silicon/1060-silicon-powder.html) | Si powder (catalog 1060) | $2–$5/g | Off-the-shelf scientific catalog; specify 45–106 µm for flow. |
| Si powder, 99.9999% (6N), –200 mesh | [American Elements](https://www.americanelements.com/silicon-powder-7440-21-3) | Si powder | $2–$5/g (100 g) | Off-the-shelf; use higher purity when O/Fe/Cu impurities must be minimized. |
| **Al–50Si master alloy** | KBM Affilips | [Aluminium master alloys](https://www.kbmaffilips.com/) | $15–$30/kg | Excellent for Si additions ≤15 wt% (covers AlSi10Mg, AlSi7Mg, etc.); also a melt practice that bypasses the autotrickler entirely for Si. |
| Pre-alloyed AlSi10Mg, 15–45 µm | MSE Supplies | [AlSi10Mg](https://www.msesupplies.com/collections/mse-pro-aluminum-powder) | ~$200–$300/kg | Continuing baseline. |

**Recommendation.** Order coarser AEE Si (45–106 µm) to address the flow
issue, plus a 5 kg Al–50Si waffle from KBM as a clean melt-practice route.

---

### 2.7 Copper (Cu)

Cu is well-behaved in atomization and abundant from AM-grade suppliers.

| Form | Supplier | Product / page | Indicative price | Notes |
|---|---|---|---|---|
| Cu gas-atomized powder, 15–45 µm | [Sandvik Osprey](https://www.metalpowder.sandvik/) | Osprey® Cu | $60–$120/kg | Scientific AM-grade. |
| Cu spherical powder, 99.9%, 15–45 µm | [American Elements](https://www.americanelements.com/copper-powder-7440-50-8) | Cu powder, AM grade | $50–$120/kg | Scientific research catalog. |
| Cu powder, 99.9%, ≤45 µm | [Goodfellow](https://www.goodfellow.com/usa/) | Cu powder | $0.50–$2/g (100 g–1 kg) | Scientific research catalog. |
| Al–50Cu master alloy | KBM Affilips | [Aluminium master alloys](https://www.kbmaffilips.com/) | $25–$50/kg | Convenient for 2xxx-series target chemistries (Cu ≤6 wt%). |

**Recommendation.** Sandvik Osprey or American Elements spherical Cu for
direct addition; Al–50Cu master alloy for high-Cu sub-systems where atomized
Cu would dilute throughput.

---

### 2.8 Titanium (Ti)

Ti powder is reactive (DG class 4.1 in fine sizes) but standard for AM. Ti
plasma-atomized powder is the gold standard but pricey; for grain-refinement
levels of Ti (≤0.5 wt%), Al–5Ti–1B is cheaper and safer.

| Form | Supplier | Product / page | Indicative price | Notes |
|---|---|---|---|---|
| Ti CP plasma-atomized, 15–45 µm | [AP&C (GE Additive)](https://www.advancedpowders.com/) (Montreal, QC) | Ti Grade 1/2 | $200–$400/kg | Aerospace AM standard. |
| Ti CP plasma-atomized, 15–45 µm | [Tekna](https://www.tekna.com/) (Sherbrooke, QC) | Ti CP | $200–$400/kg | Alternative. |
| Ti CP gas-atomized | [TLS Technik](https://www.tls-technik.de/) (Bitterfeld, DE) | EIGA Ti | $250–$450/kg | EIGA process; lower O. |
| **Al–5Ti–1B master alloy (rod/waffle)** | **KBM Affilips** | [Aluminium master alloys](https://www.kbmaffilips.com/) | $20–$40/kg | **Default for Ti grain refinement.** Industry standard. |
| Al–10Ti master alloy | Reading Alloys / Kymera | [Reading Alloys](https://www.kymerainternational.com/business-units/reading-alloys/) | $30–$60/kg | Higher Ti content. |

**Recommendation.** Al–5Ti–1B (KBM) for routine Ti additions; AP&C plasma-Ti
only when target Ti ≥5 wt%.

---

### 2.9 Iron (Fe)

| Form | Supplier | Product / page | Indicative price | Notes |
|---|---|---|---|---|
| Fe gas-atomized, 15–45 µm | **[Höganäs AB](https://www.hoganas.com/)** (Höganäs, SE) | AHC100.29, AM-grade Fe | $5–$15/kg | World's largest Fe powder producer. |
| Fe gas-atomized, 15–45 µm | [GKN Hoeganaes](https://gknpm.com/) (Cinnaminson, NJ) | AncorAM Fe | $5–$15/kg | US-based equivalent. |
| Fe carbonyl powder, 99.5%, ≤10 µm | [BASF](https://www.basf.com/) | HQ / OM grade carbonyl Fe | $20–$50/kg | Spherical, ultra-fine. |
| Fe powder, 99.9%, –325 mesh | American Elements | [Fe powder](https://www.americanelements.com/iron-powder-7439-89-6) | $0.50–$2/g (100 g) | Research scale. |
| Al–80Fe master alloy | KBM Affilips | [Aluminium master alloys](https://www.kbmaffilips.com/) | $15–$30/kg | If targeting Al-Fe-Si or quasicrystalline systems. |

**Recommendation.** Höganäs AHC100.29 for general Fe additions; BASF carbonyl
Fe if fine PSD is desired for fast melt-in.

---

### 2.10 Nickel (Ni)

| Form | Supplier | Product / page | Indicative price | Notes |
|---|---|---|---|---|
| Ni gas-atomized, 15–45 µm | [Carpenter Additive](https://www.carpenteradditive.com/) (Philadelphia, PA) | CarTech Ni 200 / 625 | $80–$150/kg | US AM-grade. |
| Ni gas-atomized, 15–45 µm | [Sandvik Osprey](https://www.metalpowder.sandvik/) (Neath, UK) | Osprey® Ni | $80–$150/kg | Established AM supplier. |
| Ni carbonyl powder (Type 123), 99.7%, 3–7 µm | [Vale](https://www.vale.com/) (Sudbury, ON) | INCO Type 123 | $40–$80/kg | Spherical, ultra-fine. |
| Ni powder, 99.9%, –325 mesh | American Elements | [Ni powder](https://www.americanelements.com/nickel-powder-7440-02-0) | $1–$3/g (100 g) | Research scale. |
| Al–20Ni master alloy | KBM Affilips | [Aluminium master alloys](https://www.kbmaffilips.com/) | $20–$40/kg | For Ni additions in transition-metal-Al systems. |

**Recommendation.** Carpenter Ni 200 for general AM Ni; Vale INCO Type 123
for fine-particle melt practice.

---

### 2.11 Cerium (Ce)

Ce metal oxidizes rapidly in air (forms a gold/blue tarnish in seconds);
ships under mineral oil or Ar. Master-alloy route is the **default** —
Al–Ce master alloys (from secondary-phase-strengthened alloy lines like
Eck Industries' Al-Ce family) are well established.

| Form | Supplier | Product / page | Indicative price | Notes |
|---|---|---|---|---|
| **Al–10Ce master alloy** | **KBM Affilips** | [Aluminium master alloys](https://www.kbmaffilips.com/) | $40–$80/kg (alloy basis) | **Default route.** Note: Eck Industries / ORNL pioneered the Al-Ce alloy system; commercial Al-Ce master alloys are available. |
| Al–10Ce / Al–20Ce master alloy | [Treibacher Industrie AG](https://www.treibacher.com/) (Althofen, AT) | Al-RE master alloys | quote | Major rare-earth metallurgy house. |
| Mischmetal (Ce-rich, ~50% Ce + La) | Treibacher; [Stanford Advanced Materials](https://www.samaterials.com/) | mischmetal | $30–$60/kg | Cheaper Ce source if Ce/La ratio is acceptable. |
| Ce metal, 99.9%, in mineral oil | American Elements | [Ce metal](https://www.americanelements.com/cerium-7440-45-1) | $5–$15/g (100 g) | Ingot only; not a powder feedstock. |
| Ce powder, 99.9%, ≤45 µm | [Heeger Materials](https://heegermaterials.com/) | Ce metal powder | quote (~$10–$25/g) | Specialty rare-earth supplier. |

**Recommendation.** Al–10Ce master alloy (KBM or Treibacher). Mischmetal if
target sub-systems explicitly include La.

---

### 2.12 Scandium (Sc)

Sc is the **highest-cost element in the palette** (spot ~$3,200/kg for 99.99%
Sc metal as of 2026-Q2). Master-alloy route is the **only sensible choice
for routine work**; elemental Sc powder is reserved for ultra-high-purity
single-composition validation.

| Form | Supplier | Product / page | Indicative price | Notes |
|---|---|---|---|---|
| **Al–2Sc master alloy** | **KBM Affilips** | [Aluminium master alloys](https://www.kbmaffilips.com/) | ~$200–$400/kg (alloy basis) ≈ $10–$20/g of Sc | **Default route.** Industry-standard form; notched waffle ingot ~7 kg. AlSc 2 grade is the workhorse. |
| Al–2Sc master alloy | [AMG Aluminum](https://amg-al.com/) | AMG Al-Sc | ~$200–$400/kg | US-based equivalent. |
| Al–2Sc master alloy | [Stanford Advanced Materials](https://www.samaterials.com/) | Al-Sc master alloy | ~$200–$400/kg | Smaller-quantity friendly. |
| Sc metal powder, 99.9%, ≤45 µm, Ar-packed | [American Elements](https://www.americanelements.com/scandium-powder-7440-20-2) | Sc powder | $30–$60/g (10 g) | High-purity validation only. |
| Sc metal powder, 99.99% | [Heeger Materials](https://heegermaterials.com/) | Sc metal powder | quote (~$50/g) | Specialty rare-earth supplier. |

**Recommendation.** Al–2Sc waffle from KBM Affilips covers the entire Phase I
Sc demand at a fraction of the cost of elemental Sc. Note: NioCorp (Elk Creek,
NE), Rio Tinto (QC, Sc as TiO₂ by-product), and Scandium International are
emerging US/CA upstream Sc producers — relevant to Genesis Mission supply-chain
narrative.

---

### 2.13 Lithium (Li)

Li metal is **air- and water-reactive** (UN 1415 Class 4.3); ships only as
ribbon/foil under Ar or in mineral oil, or pre-alloyed. Elemental Li powder
is essentially non-procurable for university labs in safe form. Master-alloy
route is **mandatory**.

| Form | Supplier | Product / page | Indicative price | Notes |
|---|---|---|---|---|
| **Al–3Li or Al–4Li master alloy (ingot)** | [FMC Lithium / Livent / Arcadium Lithium](https://www.arcadiumlithium.com/) (Philadelphia, PA) | Al-Li specialty alloys | quote | **Mandatory route.** Direct supplier of Al-Li for AA2090/2099/2195 production. |
| Al–3Li master alloy | KBM Affilips | [Aluminium master alloys](https://www.kbmaffilips.com/) | quote | European source. |
| Li metal ribbon, 99.9%, in mineral oil | [Sigma-Aldrich / Millipore Sigma](https://www.sigmaaldrich.com/US/en/product/aldrich/265985) | 265985 | $1–$3/g (10–25 g) | For glove-box compounding only; not for direct atomization. |

**Recommendation.** Al–3Li or Al–4Li master alloy ingot from Arcadium (FMC/
Livent successor) or KBM. Coordinate with AMAZEMET on rePOWDER cleaning
protocol — Li residues require argon-purged crucible work.

---

### 2.14 Erbium (Er)

Heavy rare-earth; Er is studied as an Al-alloy strengthener (similar role to
Sc, lower cost per atomic %). Master-alloy route is the **default**.

| Form | Supplier | Product / page | Indicative price | Notes |
|---|---|---|---|---|
| **Al–10Er master alloy** | **KBM Affilips** | [Aluminium master alloys](https://www.kbmaffilips.com/) | quote (~$80–$150/kg alloy basis) | **Default route.** Specialty product; quote required. |
| Al–10Er master alloy | Treibacher Industrie | [Treibacher RE master alloys](https://www.treibacher.com/) | quote | Major RE metallurgy house. |
| Er metal powder, 99.9%, ≤45 µm, Ar-packed | American Elements | [Er powder](https://www.americanelements.com/erbium-powder-7440-52-0) | $10–$20/g (100 g) | Ar-packed; for direct dosing only. |
| Er metal powder | [Edgetech Industries](https://www.edge-techind.com/) | Er metal | quote (~$10–$20/g) | RE specialist. |
| Er metal powder | Heeger Materials | [Er metal powder](https://heegermaterials.com/) | quote | RE specialist. |

**Recommendation.** Al–10Er master alloy from KBM or Treibacher. Reserve
elemental Er for limited-target sub-systems (e.g., Al–Er–Zr Sc-substitution
studies).

---

### 2.15 Zinc (Zn)

Zn is well-behaved (low MP 419.5 °C, atomizes easily, low cost), but vapor
pressure during atomization is high — mind crucible temperature.

| Form | Supplier | Product / page | Indicative price | Notes |
|---|---|---|---|---|
| Zn gas-atomized powder, 15–45 µm | [Umicore](https://www.umicore.com/en/) (Brussels, BE) | spherical Zn | $20–$50/kg | World leader in Zn metallurgy. |
| Zn gas-atomized powder, 15–63 µm | [US Zinc / EverZinc](https://www.everzinc.com/) (Houston, TX) | Zn powder | $20–$50/kg | US-based. |
| Zn dust, 99.9%, ≤10 µm | American Elements | [Zn powder](https://www.americanelements.com/zinc-powder-7440-66-6) | $0.20–$1/g (100 g–1 kg) | Standard catalog. |
| Al–50Zn master alloy | KBM Affilips | [Aluminium master alloys](https://www.kbmaffilips.com/) | $15–$30/kg | For high-Zn (7xxx-class) sub-systems. |

**Recommendation.** US Zinc spherical Zn for direct addition; Al–50Zn master
alloy when target Zn ≥5 wt% (covers 7xxx-class targets).

---

### 2.16 Tin (Sn)

| Form | Supplier | Product / page | Indicative price | Notes |
|---|---|---|---|---|
| Sn gas-atomized powder, 15–45 µm | [Indium Corporation](https://www.indium.com/products/) (Clinton, NY) | spherical Sn powder | $40–$80/kg | US AM-grade. |
| Sn spherical powder, 99.9%, 15–45 µm | [American Elements](https://www.americanelements.com/tin-powder-7440-31-5) | Sn powder, AM grade | $40–$80/kg | Scientific research catalog. |
| Sn powder, 99.85%, –325 mesh | [Goodfellow](https://www.goodfellow.com/usa/) | Sn powder | $0.50–$2/g (100 g) | Scientific research catalog. |
| Al–25Sn master alloy | KBM Affilips | [Aluminium master alloys](https://www.kbmaffilips.com/) | $30–$60/kg | For bearing-alloy-class sub-systems. |

**Recommendation.** Indium Corp spherical Sn for direct addition.

---

## 3. Master-Alloy Strategy Summary

For the **hard cases** (reactive, expensive, or unflowable), the alloying
element is best delivered as an Al-X master alloy. **Powder-only delivery
preference** (PI direction, 2026-05) plus the **no-Valimet-by-default**
direction (2026-06) mean each master alloy below should be procured, in
priority order: (i) **off-the-shelf catalog powder** from a scientific / AM
supplier (American Elements, Stanford Advanced Materials, Heeger, Treibacher)
where listed; (ii) a custom **atomized SKU** from an AM-powder producer
(Sandvik Osprey, Carpenter Additive, Elementum 3D, AP&C, Tekna — on quote,
~$200–$500/kg premium) when no catalog powder exists at the needed PSD; and
only (iii) **as a last resort**, an ingot from KBM Affilips / AMG / Reading
Alloys toll-atomized by Valimet (funded partner; adds ~2–4
weeks). These powders are then dosed and **ultrasonically atomized in-house on
the AMAZEMET rePOWDER** (induction crucible module) — the immediate,
small-quantity composition-iteration route. Valimet gas atomization remains a
parallel scale-up track for a subset of production-scale lots, not the
immediate procurement focus (proposal lines 849–854).

| Master alloy | Delivered form | Primary powder source (catalog / atomized SKU) | Fallback (last resort) | Phase I priority |
|---|---|---|---|---|
| Al–10Zr | 15–63 µm powder | Off-the-shelf elemental Zr powder (American Elements / Goodfellow); Al–Zr atomized SKU on quote (Sandvik Osprey) | KBM / AMG ingot → Valimet toll | **Tier 1** (focus system) |
| Al–25Mn | 15–63 µm powder | Off-the-shelf elemental Mn powder (American Elements / SAM) | KBM / AMG ingot → Valimet toll | **Tier 1** (focus system) |
| Al–20Cr | 15–63 µm powder | Off-the-shelf elemental Cr powder (American Elements / SAM) | KBM / AMG ingot → Valimet toll | **Tier 1** (focus system) |
| Al–2Sc | 15–63 µm powder | Catalog Al–Sc / Sc powder (SAM, American Elements); atomized SKU on quote (Sandvik Osprey / Carpenter Additive) | KBM / AMG ingot → Valimet toll | Tier 2 (expensive — buy 1 kg powder to start) |
| Al–5Ti–1B | 15–63 µm powder | Atomized SKU on quote (Sandvik Osprey / AP&C); catalog elemental Ti powder | KBM rod → Valimet toll | Tier 2 (Ti grain refinement default) |
| Al–10Ce | 15–63 µm powder | Catalog Al–Ce / Ce powder (Treibacher, Heeger, American Elements); Elementum 3D AM SKU on quote | KBM / Treibacher ingot → Valimet toll | Tier 3 |
| Al–10Er | 15–63 µm powder | Catalog Al–Er / Er powder (Treibacher, Heeger, American Elements) | KBM / Treibacher ingot → Valimet toll | Tier 3 |
| Al–3Li or Al–4Li | 15–63 µm powder (Ar-packed) | Arcadium Al-Li specialty alloy as powder on quote (Ar protocol) | Arcadium / KBM ingot → Valimet toll under Ar | Tier 3 (mandatory route; coordinate hazmat early) |
| Al–10Mg | 15–63 µm powder | Off-the-shelf coarse elemental Mg powder (Goodfellow); catalog Al–Mg | KBM / AMG ingot → Valimet toll | Optional (covers ≤2 wt% Mg) |
| Al–50Cu | 15–63 µm powder | Off-the-shelf spherical Cu powder (American Elements / Sandvik Osprey) | KBM / AMG ingot → Valimet toll | Optional |
| Al–50Si | 15–63 µm powder | Off-the-shelf coarse Si powder (Micron Metals / SAM); bypasses fine-Si flow issue | KBM / AMG ingot → Valimet toll | Optional (bypasses fine-Si flow issue) |
| Al–50Zn | 15–63 µm powder | Off-the-shelf spherical Zn powder (EverZinc / American Elements) | KBM / AMG ingot → Valimet toll | Optional (≥5 wt% Zn targets) |

---

## 4. Indicative Procurement Budget

Two tiers, per PI direction (2026-06): **§4.A is the actionable ~$2–5K
startup-fund round** to get initial in-house ultrasonic atomization runs going;
**§4.B is the full Phase I award-scope reference (~$24K)** kept for context once
the DOE award M&S budget is available. Neither is a formal budget submission.

### 4.A. Round-1 startup-fund bundle (~$2–5K, actionable now)

Sized to the AMAZEMET rePOWDER **~50 g/run** charge, so research-quantity
(50–500 g) lots of off-the-shelf catalog powder cover many composition-iteration
runs on the Al–Mn–Cr–Zr / Al–Zr focus systems. All prices indicative USD,
2026-Q2.

| Item | Lot | Indicative cost (USD) |
|---|---|---|
| High-purity Al 4N powder (1199-equivalent matrix) — American Elements / SAM | 500 g | ~$700–1,000 |
| Elemental Mn powder, coarse (American Elements / SAM) | 100 g | ~$80–150 |
| Elemental Cr powder, coarsest (American Elements / SAM) | 100 g | ~$75–160 |
| Elemental Zr powder, water-wet, DG 4.2 (American Elements / Goodfellow) | 100 g | ~$250–450 |
| Coarse Si powder, 45–106 µm (Heeger / Micron Metals) | 250 g | ~$150–300 |
| DG / hazmat shipping (Zr) + Ar-purged packaging | — | ~$100–300 |
| **Core five subtotal (minimum viable — runs going)** | | **~$1,500–2,500** |
| *Optional:* extra Al matrix (+500 g) + larger Mn/Cr/Zr lots (250 g each) | | ~$1,100–1,400 |
| *Optional:* Al–2Sc small powder lot (50–100 g, American Elements / SAM) | 50–100 g | ~$300–600 |
| *Optional:* Al–5Ti–1B powder (atomized SKU on quote) | 100–250 g | ~$200 |
| *Separate (non-powder):* 1199 Al billet for crucible / vial stock (McMaster) — use existing lab stock first | small round | ~$100–200 |
| **Round-1 startup-fund envelope** | | **~$2,000–5,000** |

This is the only spend funded from startup money right now. It deliberately
defers Mg, Cu, Ti (beyond grain refiner), Fe, Ni, Zn, Sn, Ce, Er, Li — and any
larger Sc buy — to the award-funded round in §4.B.

### 4.B. Full Phase I award-scope reference (~$24K, once DOE M&S funds available)

Kept for planning context only — **do not order against this until the Phase I
award M&S budget is in hand.** Tied to the FLAIME budget line "Al alloy
elemental powders and high-purity Al crucibles for atomization" (proposal
§Budget, ~$35K M&S allocation).

| Item | Lot | Indicative cost (USD) |
|---|---|---|
| High-purity Al 4N powder (1199-equivalent, Tier 1 base) — American Elements / SAM | 1–2 kg | ~$3,000 |
| 1199 Al billet stock (99.99%, crucibles, McMaster — non-powder) | ~50 lb | ~$1,500 |
| Elemental Mn powder (American Elements / SAM, coarse) | 500 g | ~$800 |
| Elemental Cr powder (American Elements / SAM, coarsest) | 500 g | ~$1,500 |
| Elemental Zr powder, water-wet (American Elements / Goodfellow) | 250 g | ~$2,000 |
| Coarse Si powder, 45–106 µm (Micron Metals / SAM / American Elements) | 1 kg | ~$1,000 |
| Al–2Sc master-alloy powder (catalog / atomized SKU on quote) | 1 kg | ~$2,500 |
| Al–5Ti–1B master-alloy powder (atomized SKU on quote) | 1 kg | ~$500 |
| Mg, Cu, Fe, Ni, Zn, Sn elemental powders (American Elements / Goodfellow / Höganäs / EverZinc / Indium) | 1–5 kg each | ~$1,200 |
| Al–10Ce, Al–10Er master-alloy / RE powders (Treibacher / Heeger / American Elements) | 0.5–1 kg each | ~$700 |
| Arcadium Al–3Li master-alloy powder (Ar protocol, on quote) | 0.5 kg | quote (~$1,500) |
| Valimet toll-atomization (contingency only, if a needed PSD is unavailable off-the-shelf) | as needed | [partner rate removed] |
| Hazmat / DG shipping surcharges, Ar-purged packaging contingency | — | ~$1,500 |
| **Subtotal (indicative, off-the-shelf powder-form)** | | **~$18,200** |
| Contingency (30%) for quotes / lead-time / rare-earth spot moves | | ~$5,500 |
| **Award-scope Phase I powder M&S envelope** | | **~$23,700** |

The award-scope envelope is off-the-shelf catalog powder from scientific
suppliers (American Elements, Stanford Advanced Materials) rather than ingot +
Valimet toll-atomization (removed from the critical path per PI direction,
2026-06), comfortably inside the proposal's ~$35K M&S allocation, with ~$11K
headroom for crucible machining, consumables, hazmat shipping, custom
atomized-SKU premiums, and a mid-Phase-I top-up.

---

## 5. Vendor Directory (validated canonical URLs)

### Primary (recommended)

| Vendor | HQ | Role for FLAIME | URL |
|---|---|---|---|
| **American Elements** | Los Angeles, CA, USA | **Primary** off-the-shelf catalog elemental & alloy powders (all 16 elements) | https://www.americanelements.com/ |
| **Stanford Advanced Materials** | Lake Forest, CA, USA | **Primary** off-the-shelf catalog elemental, RE & master-alloy powders | https://www.samaterials.com/ |
| **AMAZEMET** | Warsaw, PL | Funded partner; rePOWDER ultrasonic atomizer — **immediate in-house small-quantity atomization route** (proposal lines 849–854) | https://www.amazemet.com/ |
| **Valimet** | Stockton, CA, USA | Funded partner; Al / ingot gas atomization — **production-scale scale-up track, parallel not immediate**; toll-atomization is contingency only | https://valimet.com/ |
| **KBM Affilips** | Beerse, BE | Master-alloy metallurgy (request atomized SKU; ingot → toll-atomize as fallback) | https://www.kbmaffilips.com/ |
| **AMG Aluminum** | Wayne, PA, USA | US-based master-alloy backup | https://amg-al.com/ |
| **Reading Alloys / Kymera International** | Robesonia, PA, USA | US-based Ti/Al master-alloy backup | https://www.kymerainternational.com/business-units/reading-alloys/ |

### Atomized AM-grade powders (elemental & specialty)

| Vendor | Specialty | URL |
|---|---|---|
| Carpenter Additive | Ni, Co, stainless | https://www.carpenteradditive.com/ |
| Sandvik Osprey | Ni, Cu, broad; custom Al-X atomized master alloys on quote | https://www.metalpowder.sandvik/en/products/ |
| AP&C (GE Additive) | Ti plasma-atomized | https://www.advancedpowders.com/ |
| Tekna | Ti, refractory plasma-atomized | https://www.tekna.com/ |
| TLS Technik | Ti EIGA | https://www.tls-technik.de/ |
| Equispheres | Al, narrow PSD | https://www.equispheres.com/ |
| Uniformity Labs | Al optimized | https://uniformitylabs.com/ |
| 6K Additive | Recycled Ni/Ti/Al | https://6kadditive.com/ |
| Elementum 3D | RAM Al/Cu/Ni; custom atomized Al master-alloy powders | https://www.elementum3d.com/materials/aluminum/ |
| Indium Corporation | Sn, In, low-MP powders | https://www.indium.com/products/ |
| MSE Supplies | AM-grade catalog | https://www.msesupplies.com/ |
| BASF | Carbonyl Fe / Ni | https://www.basf.com/ |
| Vale | INCO carbonyl Ni | https://www.vale.com/ |
| Höganäs AB | Fe (bulk reference) | https://www.hoganas.com/ |

### Rare-earth / reactive specialty

| Vendor | Specialty | URL |
|---|---|---|
| Treibacher Industrie AG | Ce, Er, Sc, mischmetal, Al-RE master alloys | https://www.treibacher.com/ |
| MP Materials | Upstream RE (Mountain Pass, CA) | https://mpmaterials.com/ |
| Lynas Rare Earths | Upstream RE | https://lynasrareearths.com/ |
| NioCorp | Sc (Elk Creek, NE — emerging US source) | https://niocorp.com/ |
| Scandium International Mining | Sc (emerging) | https://www.scandiummining.com/ |
| Heeger Materials | RE research powders | https://heegermaterials.com/ |
| Edgetech Industries | RE research powders | https://www.edge-techind.com/ |
| Stanford Advanced Materials | RE + master alloys | https://www.samaterials.com/ |
| Arcadium Lithium (Livent / FMC) | Al-Li master alloys, Li metal | https://www.arcadiumlithium.com/ |
| Luxfer MEL Technologies (Magnesium Elektron) | Mg AM powder | https://luxfermeltechnologies.com/ |
| Atlantic Equipment Engineers / Micron Metals | Cr, Si, refractory research powders | https://micronmetals.com/ |

### Elemental / wire stock (for crucibles, autotrickler feedstock)

| Vendor | Use | URL |
|---|---|---|
| McMaster-Carr | 1199 / 1100 Al billet for crucibles, fasteners | https://www.mcmaster.com/ |
| OnlineMetals | 1199 / 1100 Al wire | https://www.onlinemetals.com/ |
| Sigma-Aldrich / MilliporeSigma | Li ribbon, glove-box-grade reactives | https://www.sigmaaldrich.com/ |
| Alfa Aesar / Thermo Fisher | Catalog elemental powders | https://www.thermofisher.com/ |
| Goodfellow | Broad metals catalog | https://www.goodfellow.com/usa/ |

---

## 6. Handling & Safety Notes (summary)

| Element / form | Hazard class | Notes |
|---|---|---|
| Fine Al, Mg, Ti, Zr, Sc powders (≤45 µm) | Combustible dust / 4.1–4.2 | Argon-purged storage; grounded handling; do not vacuum with standard shop vac. |
| Zr metal powder (fine, dry) | UN 1358 (4.2, pyrophoric) | Ship water-wet; **prefer Al–10Zr master alloy**. |
| Mg powder (fine) | UN 1418 (4.3) | Coarser PSD safer; **prefer Al–10Mg master alloy** for ≤2 wt%. |
| Li metal | UN 1415 (4.3, water-reactive) | Mineral-oil packed; **prefer Al-Li master alloy**. |
| Cr powder | Generally non-flammable | Carcinogenic dust (Cr(VI) potential on heating); fume hood + PAPR for atomization. |
| Ce, Er, Sc metal | Air-sensitive (Ce especially) | Ar-packed; use master alloys when possible. |
| Si fines | Combustible dust at fine PSD | Coarser (≥45 µm) preferred for autotrickler. |

All in-lab powders must have current SDS in the byu-vcl repo SDS folder
(see `alloy-workflow-review.md` §1).

---

## 7. Open Questions / Next Steps

1. **Place the Round-1 startup-fund PO first (~$2–5K, §0 / §4.A)** (PI
   direction, 2026-06): the core five off-the-shelf powders — high-purity Al 4N
   matrix, elemental Mn, Cr, water-wet Zr, and coarse 45–106 µm Si — in
   research-quantity (50–500 g) lots from
   [American Elements](https://www.americanelements.com/) and
   [Stanford Advanced Materials](https://www.samaterials.com/) (Si also from
   [Heeger](https://heegermaterials.com/silicon-powders/74-45-106-micron-spherical-silicon-si-powder.html)).
   This is sized only to seed the first handful of in-house ultrasonic
   atomization runs on the Al–Mn–Cr–Zr / Al–Zr focus systems; it is **not** the
   full award M&S budget. Also ask both suppliers whether they will provide
   **free test powders** for autotrickler dispensing trials and in-house
   characterization.
2. Place the coarse-Si **powder** order with [Micron Metals (AEE)](https://micronmetals.com/)
   (or American Elements / SAM) to immediately resolve the autotrickler flow
   problem documented in `alloy-workflow-review.md` §1.5 and
   [powder-doser#19](https://github.com/vertical-cloud-lab/powder-doser/pull/19).
3. Get quotes from **Sandvik Osprey**, **Carpenter Additive**, and
   **American Elements / SAM** for Al–2Sc and Al–5Ti–1B as off-the-shelf or
   custom-atomized 15–63 µm powder SKUs, 1 kg each.
4. Confirm AMAZEMET rePOWDER induction-crucible compatibility with each
   master alloy (Al-Li, Al-Sc, Al-Ce, Al-Er specifically — check for crucible
   reaction or vapor loss). The rePOWDER is the **immediate in-house ultrasonic
   atomization route** for small-quantity composition-iteration runs (proposal
   lines 849–854); prioritize getting these small runs going. The Valimet
   gas-atomization scale-up collaboration proceeds in parallel for a subset of
   production-scale lots, but is not the immediate procurement focus.
5. **Contingency only:** if a needed PSD is unavailable off-the-shelf, get a
   per-kg toll-atomization price and lead time from Valimet for KBM master-
   alloy ingots, and a special quote for Al–3Li under the Ar-purged hazmat
   variant. This is a fallback, not the default route.
6. Confirm whether US-only sourcing is required by the Genesis Mission
   final award terms; if so, AMG / Reading Alloys (Kymera) supersede KBM
   for master alloys.
7. Cross-link this file from `company-landscape.md` §1 and from the proposal
   §Budget M&S notes.
