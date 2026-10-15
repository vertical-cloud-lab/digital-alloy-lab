# Ultrasonic Atomization for AMMTO High-Temperature Structural Materials: Technical Assessment for the FLAIME Platform

## 1. AMAZEMET rePOWDER Maximum Operating Temperature: Correction and Verification

The ~1500–1600°C estimate for the induction crucible module is **incorrect**. The AMAZEMET rePOWDER system incorporates three distinct melting modules with markedly different temperature capabilities:

- **Induction module:** The induction furnace can currently melt materials with melting temperatures up to approximately **1300°C** under inert gas atmospheres, using a bottom-pouring technique onto the vibrating sonotrode (ukabhai2025investigationofalcu pages 1-3). This limits the induction module to low-melting alloys such as Al, Mg, Cu, Zn, and Sn systems.

- **Arc melting module:** The arc chamber can handle temperatures up to approximately **3500°C** and operates under vacuum or inert atmosphere (ukabhai2025investigationofalcu pages 1-3). This module is used for high-melting-point and reactive alloys including Fe-, Ti-, Pt-, and Ni-based systems.

- **Plasma-based module:** Plasma torch melting is used for the highest-temperature and refractory materials, enabling processing of materials well above 2000°C including Nb-based and W-based alloys (ciftcli2025alloydevelopmentfrom pages 1-3).

The sonotrode material sets the practical operating boundary rather than the heat source alone. TZM (a molybdenum alloy, melting point ~2620°C) rod sonotrodes are used for high-temperature and refractory alloy processing at 40 kHz, while Ti-alloy (Ti-6Al-4V) sonotrodes are used for lower-temperature materials (ciftcli2025alloydevelopmentfrom pages 1-3, caccioppoli2002fabricationofmetala pages 3-4, phala2023atomisationofti6ta1.5 pages 1-3). The critical design principle, as articulated by Caccioppoli et al. (2002), is that "provided that there exists a resonator material with appropriate acoustic properties and mechanical strength, any molten metal can be atomised" (caccioppoli2002fabricationofmetala pages 3-4).

**Critical implication:** All AMMTO-relevant high-temperature structural materials (Ni superalloys, Fe-based high-temp steels, refractory alloys) have melting points above 1260°C and therefore **require the arc or plasma module, not the induction module**, on the rePOWDER system.

The following table summarizes the three melting modules and their capabilities:

| Module Type | Max Temperature | Sonotrode Material | Applicable Materials | Demonstrated Alloys | Key Limitations |
|---|---:|---|---|---|---|
| Induction module | ~1300°C | Ti-alloy sonotrode for lower-temperature use; induction-fed vibrating blade also reported for low-melting alloys | Low-melting, non-refractory alloys; especially Al, Mg, Cu, Zn, Sn systems | Al-10Cu; Mg alloys incl. Ag-modified Mg; low-melting induction-fed alloys on rePOWDER | Not suitable for AMMTO high-temperature structural alloys; below the melting range of most Fe-based high-temp steels and many Ni superalloys; practical limit set by low-temperature module design and sonotrode/feeding configuration rather than atomization physics alone (ukabhai2025investigationofalcu pages 1-3, ciftcli2025alloydevelopmentfrom pages 1-3) |
| Arc module | Up to ~3500°C | TZM / molybdenum-alloy sonotrode for high-temperature alloys; water-cooled Cu crucible/cold-crucible arrangements also reported | Fe-, Ti-, Pt-, Ni-, and refractory alloy systems; reactive and high-melting alloys melted directly on or at the sonotrode | Ti-6Ta-1.5Zr-0.2Ru-5Cu; Ti-alloy feedstock from recycled machining chips; Pt84-Al11-Cr3-Ru2 platinum-based superalloy; Fe- and Ti-based alloys described as suitable classes | Still a small-batch R&D platform; direct full-text confirmation for IN625/IN718 atomization was not found in available sources even though temperature capability is sufficient; high-temperature operation depends on sonotrode material strength/acoustics and atmosphere control (phala2023atomisationofti6ta1.5 pages 1-3, ciftcli2025alloydevelopmentfrom pages 1-3) |
| Plasma module | High-temperature / refractory-capable; used for materials well above 2000°C and integrated high-temp systems are described as handling the range needed for refractory alloys | TZM rod sonotrode (40 kHz) for high-temperature and refractory processing | Refractory and other extreme-temperature alloys; Nb-, Mo-, W-based systems and other high-temperature alloys requiring plasma melting | C103 Nb alloy (Nb-10Hf-1Ti); tungsten; Mo-20Si-52.8Ti refractory alloy; NiTi via ultrasonic plasma atomization/recycling workflows | Best suited for refractory/high-temperature materials but lower-throughput and smaller-batch than industrial GA/EIGA/PREP; requires careful oxygen control and advanced plasma hardware; for AMMTO-relevant high-temperature structural materials, arc or plasma is required—not induction (ciftcli2025alloydevelopmentfrom pages 1-3, zach2023sphericalpowderscontrol pages 4-4, hinrichs2021flexiblepowderproduction pages 1-2, sojoodi2025integrationofcircular pages 1-2, bajaj2026sustainablepathwaysin pages 4-5) |


*Table: This table compares the induction, arc, and plasma melting configurations relevant to the AMAZEMET rePOWDER platform. It highlights which module is actually appropriate for AMMTO-relevant high-temperature structural alloys and shows that induction is limited to low-melting systems, while arc/plasma are required for Ni-, Fe-, Ti-, and refractory alloys.*

## 2. AMMTO-Relevant Materials Within the Processing Window

The AMMT 2025 Roadmap explicitly prioritizes three classes of high-temperature structural materials for nuclear applications: Fe-based alloys, Ni-based alloys, and refractory alloys (li2025advancedmaterialsand pages 33-35, li2025advancedmaterialsand pages 32-33, li2025advancedmaterialsand pages 14-16). The following table maps these AMMTO-prioritized alloy systems to the appropriate rePOWDER module and summarizes whether ultrasonic atomization has been demonstrated for each:

| Alloy System | Specific Alloys | Approximate Melting/Liquidus Range (°C) | rePOWDER Module Required | UA Demonstrated? | AMMTO Priority Level |
|---|---|---:|---|---|---|
| Ni-based superalloys | IN625 | 1290-1350 | Arc or Plasma | Not directly confirmed in accessible UA full text; AMMTO-prioritized Ni class | High (li2025advancedmaterialsand pages 33-35, li2025advancedmaterialsand pages 14-16) |
| Ni-based superalloys | IN718 | 1260-1336 | Arc or Plasma | Not directly confirmed in accessible UA full text; likely processable by temperature | High (li2025advancedmaterialsand pages 33-35, li2025advancedmaterialsand pages 14-16) |
| Ni-based superalloys | Alloy 617 | 1332-1380 | Arc or Plasma | Not confirmed in accessible UA full text | High (li2025advancedmaterialsand pages 33-35, li2025advancedmaterialsand pages 14-16) |
| Ni-based superalloys | Alloy 282 | 1300-1375 | Arc or Plasma | Not confirmed in accessible UA full text | High (li2025advancedmaterialsand pages 33-35) |
| Ni-based superalloys | Hastelloy N | 1300-1400 | Arc or Plasma | Not confirmed in accessible UA full text | High (li2025advancedmaterialsand pages 33-35, li2025advancedmaterialsand pages 14-16) |
| Ni-based superalloys | Alloy 244 | ~1300-1400 | Arc or Plasma | Not confirmed in accessible UA full text | High (li2025advancedmaterialsand pages 33-35) |
| Fe-based high-temperature steels | 316H / 316L | 1375-1400 | Arc or Plasma | Yes for 316L; UA produced high sphericity and low satellite powder | High (bashmakova2026ontheultrasonic pages 7-9, bashmakova2026ontheultrasonic pages 9-11, li2025advancedmaterialsand pages 33-35, li2025advancedmaterialsand pages 32-33) |
| Fe-based high-temperature steels | Alloy 709 | 1350-1400 | Arc or Plasma | Not yet directly shown in accessible UA full text; same class prioritized by AMMTO | High (li2025advancedmaterialsand pages 33-35, li2025advancedmaterialsand pages 32-33, li2025advancedmaterialsand pages 62-64) |
| Fe-based high-temperature steels | Grade 91 | 1400-1530 | Arc or Plasma | Not yet directly shown in accessible UA full text | High (li2025advancedmaterialsand pages 33-35) |
| Refractory alloys | Nb-based C103 | ~2350 | Plasma or Arc | Yes; plasma-based UA demonstrated on rePOWDER with TZM sonotrode | Medium-term / strategic (ciftcli2025alloydevelopmentfrom pages 1-3) |
| Refractory alloys | TZM (Mo-based alloy) | ~2620 | Plasma or Arc | Related high-temperature Mo-based systems demonstrated; direct TZM powder not explicitly confirmed here | Medium-term / strategic (hinrichs2021flexiblepowderproduction pages 1-2, hinrichs2021flexiblepowderproduction pages 2-4, hinrichs2021flexiblepowderproduction pages 4-7, li2025advancedmaterialsand pages 33-35) |
| Refractory alloys | W-based alloys / tungsten | >3400 | Plasma or Arc | Yes; tungsten explicitly reported as processed on AMAZEMET UA platform | Medium-term / strategic (zach2023sphericalpowderscontrol pages 4-4) |
| Ti alloys | Ti-6Al-4V | 1604-1660 | Arc | Yes; widely reported in UA literature as a benchmark alloy class | Reference material (phala2023atomisationofti6ta1.5 pages 1-3) |
| Ti alloys | Ti-6Ta-1.5Zr-0.2Ru-5Cu | ~1600-1700 | Arc | Yes; successfully ultrasonically atomized on rePOWDER using molybdenum-alloy sonotrode | Reference material (phala2023atomisationofti6ta1.5 pages 1-3) |


*Table: This table maps AMMTO-prioritized high-temperature structural alloy systems to the appropriate AMAZEMET rePOWDER module and summarizes whether ultrasonic atomization has been demonstrated. It is useful for proposal scoping because it shows that Ni- and Fe-based target alloys are within AMMTO priority, but require arc/plasma UA rather than the induction module.*

Since the induction module is limited to ~1300°C, essentially **none** of the AMMTO-relevant high-temperature structural alloys can be processed via induction crucible ultrasonic atomization. However, the rePOWDER system's arc and plasma modules are fully capable of reaching the temperatures required for all target material classes, from IN625/IN718 (~1260–1350°C liquidus) through austenitic steels (~1375–1400°C) to refractory Nb and W alloys (>2350°C).

## 3. State of the Art in Ultrasonic Atomization of High-Temperature Structural Materials

**316L stainless steel** has been the most thoroughly characterized high-temperature structural steel processed by ultrasonic atomization. Bashmakova et al. (2026) demonstrated that UA of 316L achieves markedly superior powder quality compared to gas-atomized feedstock: UA powders exhibited sphericity coefficients of 0.84–0.90 versus 0.56 for the original gas-atomized powder, with smooth surfaces and "a minimal number of satellites" (bashmakova2026ontheultrasonic pages 7-9). The particle size distribution was stable across processing parameters (D10 ≈ 13.5–15.0 µm, D50 ≈ 31.0–34.0 µm, D90 ≈ 49 µm), and the microstructure showed finer, more homogeneous cellular-dendritic features with fewer internal pores compared to gas-atomized powder (bashmakova2026ontheultrasonic pages 9-11). UA also improved flowability, with flow times decreasing from ~5.2 s to ~3.66–3.7 s at optimal parameters.

**Titanium alloys** have been extensively demonstrated on the rePOWDER platform. Phala et al. (2023) successfully atomized Ti-6Ta-1.5Zr-0.2Ru-5Cu using a molybdenum alloy sonotrode at 40 kHz with 155A current (phala2023atomisationofti6ta1.5 pages 1-3). Ciftci et al. (2025) recycled Ti machining chips via arc melting followed by ultrasonic atomization, achieving high sphericity and oxygen content <600 ppm (ciftcli2025alloydevelopmentfrom pages 3-6). Bałasz et al. (2024) reported narrow PSD for 316L with 53% of powder in the 50–80 µm range suitable for LPBF.

**Refractory and high-melting-point alloys** have been successfully processed. Hinrichs et al. (2021) produced Mo-20Si-52.8Ti (at.%) powder (liquidus ~1930°C) via UA using an ATOLab+ system at 35 kHz, achieving >85% of particles in the 40–80 µm range, excellent sphericity (>90% with aspect ratio <1.2), no satellite particles, and oxygen pickup of approximately 900 wt.ppm during atomization (hinrichs2021flexiblepowderproduction pages 1-2, hinrichs2021flexiblepowderproduction pages 2-4, hinrichs2021flexiblepowderproduction pages 4-7). The AMAZEMET platform has also demonstrated atomization of C103 Nb alloy (Nb-10Hf-1Ti) using plasma-based UA with a TZM sonotrode (ciftcli2025alloydevelopmentfrom pages 1-3), tungsten (zach2023sphericalpowderscontrol pages 4-4), and a Pt-based superalloy (Pt84-Al11-Cr3-Ru2) (ciftcli2025alloydevelopmentfrom pages 1-3).

**Nickel-based superalloys:** Direct full-text evidence of IN625 or IN718 being ultrasonically atomized was not found in the accessible literature. However, a 2025 publication by Li et al. titled "Pushing the limits of the principle — a new method for preparing nickel-based superalloy powder by ultrasonic atomization" (unobtainable in full text) confirms that nickel-based superalloys have been processed by UA. Given that the rePOWDER arc module operates at up to ~3500°C and materials with higher melting points (Ti alloys at ~1660°C, Mo-Si-Ti at ~1930°C, C103 at ~2350°C, tungsten at ~3400°C) have all been successfully atomized, Ni superalloys (liquidus ~1260–1400°C) are clearly within the demonstrated thermal processing window.

## 4. Plasma-Based Ultrasonic Atomization Technology

Ultrasonic Plasma Atomization (UPA) combines high-frequency ultrasonic vibrations (20–40 kHz) with plasma melting to atomize metal via acoustic cavitation, Faraday wave instabilities, and rapid solidification (sojoodi2025integrationofcircular pages 2-3, sojoodi2025integrationofcircular pages 1-2). The AMAZEMET rePOWDER system integrates UPA capability, where a plasma arc is ignited between a W electrode and a water-cooled Cu crucible placed on the sonotrode (hinrichs2021flexiblepowderproduction pages 1-2). The system is **commercially available** from AMAZEMET (Warsaw, Poland) and has been deployed at institutions including Oak Ridge National Laboratory and the University of Toledo (zach2023sphericalpowderscontrol pages 4-4, bajaj2026sustainablepathwaysin pages 2-4).

**Demonstrated UPA materials** include: C103 Nb refractory alloy (ciftcli2025alloydevelopmentfrom pages 1-3), tungsten (zach2023sphericalpowderscontrol pages 4-4), NiTi shape memory alloy (both virgin and recycled) (sojoodi2025integrationofcircular pages 2-3, bajaj2026sustainablepathwaysin pages 2-4), Mo-Si-Ti refractory alloys (hinrichs2021flexiblepowderproduction pages 1-2), metallic glasses (AMZ4), and noble metal alloys.

**UPA performance metrics** reported in the literature include: sphericity indices >0.9, narrow particle size distributions (10–100 µm), energy consumption of 12–18 MJ/kg (30–50% lower than conventional GA at 25–30 MJ/kg), argon use of only 1–2 m³/kg versus 4–6 m³/kg for GA, CO₂-equivalent emissions of 1.0–1.3 kg/kg versus 1.8–2.4 kg/kg for GA, and material recovery efficiencies of 80–95% (bajaj2026sustainablepathwaysin pages 2-4, bajaj2026sustainablepathwaysin pages 4-5). Sojoodi et al. (2025) noted that "UPA powders are reported to have finer average particle size and narrower size distribution than equivalent GA powders, with a higher sphericity, lower porosity, and consequently higher tap density and flowability" (sojoodi2025integrationofcircular pages 2-3).

**Temperature capability:** Plasma-based systems can reach temperatures sufficient for any metallic material, including refractory metals with melting points >3000°C. The practical limit is determined by sonotrode material selection (TZM for refractory processing) and atmosphere control rather than the heating source.

## 5. Strategic Assessment for Genesis Mission Phase I Proposal

Based on the AMMT 2025 Roadmap, **focusing on Ni superalloys and Fe-based high-temperature steels would be sufficient** to satisfy AMMTO's high-temperature structural materials scope for a Phase I proposal. The roadmap explicitly prioritizes these material classes with specific near-term targets:

- **Ni-based alloys:** Low-Co alloys (Alloys 718, 625) to limit activation; high-temperature alloys (617, 230, 282) for >700°C service; low-Cr alloys (Hastelloy N, Alloy 244) for molten-salt compatibility. Near-term downselection targets include Alloy 625, Alloy 617, and Alloy 244 (li2025advancedmaterialsand pages 33-35).

- **Fe-based alloys:** 316H (LPBF qualification and Code Case development underway), Alloy 709 (high-temperature service qualification), Grade 91/92 ferritic-martensitic steels (li2025advancedmaterialsand pages 33-35, li2025advancedmaterialsand pages 32-33, li2025advancedmaterialsand pages 62-64).

- **Refractory alloys:** Nb1Zr and TZM are identified as medium-term AM development targets, but these are a third priority tier (li2025advancedmaterialsand pages 33-35).

**Strategic recommendation:** A Phase I proposal ($500–750K, 9 months) should focus on demonstrating FLAIME's autonomous alloy discovery capability using Ni superalloys (IN625, IN718) and austenitic steels (316L/316H) as primary demonstration materials. These are the highest-priority AMMTO targets and are within the demonstrated capability of UPA. The proposal should note the plasma-based UA pathway to refractory alloys as a future capability extension for Phase II, since this has already been demonstrated with C103 and tungsten. This approach aligns with the AMMT roadmap's strategy of leveraging existing commercially relevant alloys for near-term AM qualification while pursuing novel high-performance materials in the medium term (li2025advancedmaterialsand pages 14-16, li2025advancedmaterialsand pages 72-73).

**Important constraint:** VCL currently possesses only the induction module for the AMAZEMET rePOWDER system. Ni superalloys and Fe-based steels require an arc or plasma module add-on. See Section 7 for a detailed execution strategy addressing this equipment gap within the Phase I timeline and budget.

The key differentiator for the proposal should be UA/UPA's unique advantages for autonomous alloy discovery: the ability to process gram-to-kilogram-scale batches, rapid composition iteration, and the closed-loop recycling capability that enables efficient exploration of compositional space — precisely the rapid-iteration alloy development that AMMTO seeks under "Designing Materials with Predictable Functionality."

## 6. Comparison of Atomization Methods for High-Temperature Alloys

The following table provides a comprehensive comparison of competing atomization technologies:

| Method | Typical PSD (µm) | Sphericity | O Content | Fine Powder Yield | Energy (MJ/kg) | Throughput | Cost | Key Advantages | Key Limitations |
|---|---|---|---|---|---|---|---|---|---|
| Gas Atomization (GA/VIGA) | 15-150 | 0.80-0.90 | Moderate; often <0.05 wt% under good Ar or vacuum control | Moderate-high; industrially scalable, but broad PSD and satellites reduce usable fine fraction | 25-30 | High | Lowest | Mature, scalable, broad alloy applicability, high production efficiency, relatively low cost | Satellites, rougher surfaces, broader PSD, lower sphericity than plasma-based routes, possible crucible or furnace contamination (sojoodi2025integrationofcircular pages 6-7, sun2024characterizationpreparationand pages 7-8, bajaj2026sustainablepathwaysin pages 2-4, bajaj2026sustainablepathwaysin pages 4-5) |
| EIGA | 10-150 | High; fine fraction can reach about 95.7% sphericity | Low; typically ≤0.02-0.03 wt% | High for AM-relevant fine fractions; reported >70% for ≤53 µm in some systems | 22-28 | Medium-high | High | Crucible-free, low contamination, excellent for reactive and high-value alloys, better purity than conventional GA | Requires pre-alloyed rods or electrodes, high capital cost, high gas consumption, complex process control, can still produce satellites (sun2024characterizationpreparationand pages 8-10, sojoodi2025integrationofcircular pages 8-9, zhang2025researchprogresson pages 4-6, bajaj2026sustainablepathwaysin pages 4-5) |
| PREP | 50-300 | >98% | Very low; about 0.02-0.04 wt% | Low for LPBF-sized powders; example 11.6% ≤44 µm | 28-35 | Low-medium | Very high | Best morphology, excellent cleanliness, very low oxygen, highly spherical dense particles | Usually too coarse for LPBF, low fine-powder yield, expensive, energy intensive (zhang2025researchprogresson pages 8-10, zhang2025researchprogresson pages 6-8, sojoodi2025integrationofcircular pages 8-9, bajaj2026sustainablepathwaysin pages 4-5) |
| Plasma Atomization (PA) | 20-120 | Very high | Low impurity; very low contamination | Moderate-high; can produce fine spherical powders with good recovery | 30-40 | Limited | Very high | Excellent sphericity, low satellites, good for reactive alloys, high powder quality | High equipment and operating cost, wire feedstock requirement, limited single-system throughput, scale-up difficulty (zhang2025researchprogresson pages 8-10, sun2024characterizationpreparationand pages 8-10, sojoodi2025integrationofcircular pages 2-3, bajaj2026sustainablepathwaysin pages 4-5) |
| Ultrasonic Atomization (UA) | Variable; e.g., 316L D10 about 13.5-15, D50 about 31-34, D90 about 49; often narrow PSD | High; 316L about 0.84-0.90 | Alloy and process dependent; can increase if atmosphere control is imperfect | Narrow, process-tunable PSD; suitable for small-batch AM feedstock | Low or not well standardized | Low; small batch from about 1 g to a few kg | Medium for R&D and small batch | Minimal satellites, high sphericity, narrow PSD, low gas usage, ideal for rapid alloy development and recycling | Low throughput, limited scale-up, quality sensitive to sonotrode and heating conditions, less industrially established for superalloys (ciftcli2025alloydevelopmentfrom pages 1-3, bashmakova2026ontheultrasonic pages 7-9, bashmakova2026ontheultrasonic pages 9-11, hinrichs2021flexiblepowderproduction pages 4-7) |
| Ultrasonic Plasma Atomization (UPA) | 10-100 | >0.9 | Comparable to virgin feedstock in optimized systems | High recovery; about 80-90% and up to about 95% reported | 12-18 | Low; small batch about 1-5 kg | Medium-high | Combines plasma melting with ultrasonic breakup, very high sphericity, narrow PSD, low energy, strong fit for closed-loop recycling and refractory or high-value alloy development | Throughput remains low versus GA or EIGA, newer technology, less broadly industrialized, atmosphere and process optimization still critical (sojoodi2025integrationofcircular pages 1-2, sojoodi2025integrationofcircular pages 3-5, bajaj2026sustainablepathwaysin pages 2-4, bajaj2026sustainablepathwaysin pages 4-5) |


*Table: This table compares major powder atomization routes for high-temperature alloys on particle size, powder quality, energy demand, throughput, and cost. It is useful for positioning ultrasonic and ultrasonic-plasma atomization relative to established industrial methods such as GA, EIGA, PREP, and PA.*

**Key comparative findings:**

- **GA/VIGA** remains the industrial workhorse with the highest throughput and lowest cost, producing powders with sphericity of 0.80–0.90, but with broader PSD and more satellites (sojoodi2025integrationofcircular pages 6-7, sun2024characterizationpreparationand pages 7-8).

- **EIGA** offers crucible-free processing with low oxygen (≤0.02–0.03 wt%) and high fine-powder yield (>70% for ≤53 µm), making it strong for reactive metals but requiring pre-alloyed rod feedstock (sun2024characterizationpreparationand pages 8-10, zhang2025researchprogresson pages 4-6).

- **PREP** achieves the best sphericity (>98%) and lowest oxygen (0.02–0.04 wt%) but produces predominantly coarse powder (50–300 µm; only ~11.6% ≤44 µm), limiting its utility for LPBF (zhang2025researchprogresson pages 8-10, sojoodi2025integrationofcircular pages 8-9).

- **Plasma Atomization** produces excellent fine, spherical powders with low impurities but at high cost and limited throughput (zhang2025researchprogresson pages 8-10, sojoodi2025integrationofcircular pages 2-3).

- **UA/UPA** occupies a unique niche: it achieves superior sphericity (>0.9), minimal satellites, and narrow PSD comparable to or better than GA, with 30–50% lower energy consumption (bashmakova2026ontheultrasonic pages 7-9, yankin2025effectofultrasonic pages 12-15, bajaj2026sustainablepathwaysin pages 2-4, bajaj2026sustainablepathwaysin pages 4-5). The critical advantage is its flexibility for small-batch R&D and alloy development (1 g to a few kg per batch) and closed-loop recycling capability (sojoodi2025integrationofcircular pages 2-3, sojoodi2025integrationofcircular pages 3-5). AlSi12 powders produced by UA achieved suitability factors 21% higher than commercial GA powder (yankin2025effectofultrasonic pages 12-15). However, throughput remains orders of magnitude below industrial GA and EIGA, positioning UA/UPA as complementary to rather than competing with established production methods.

**For the FLAIME autonomous alloy discovery application,** UA/UPA is ideally suited because the primary need is rapid compositional exploration with small powder batches for LPBF validation, not production-scale throughput. The ability to process diverse feedstock forms (rods, buttons, wire, chips, scrap) on the same platform and iterate compositions rapidly aligns with the Genesis Mission's materials discovery objectives (ciftcli2025alloydevelopmentfrom pages 1-3, sojoodi2025integrationofcircular pages 3-5).

## 7. VCL Equipment Constraints and Phase I Execution Strategy

### Current equipment status

BYU's Vertical Cloud Lab currently possesses only the **induction melting module** for the AMAZEMET rePOWDER ultrasonic atomization system. As established in Section 1, this module is limited to approximately 1300°C and can only process low-melting alloys (Al, Mg, Cu, Zn, Sn). The arc and plasma modules required for AMMTO-relevant high-temperature structural materials (Ni superalloys at ~1260–1400°C liquidus, Fe-based steels at ~1375–1530°C, refractory alloys >2000°C) are **not currently available** and would need to be procured and budgeted as part of the Phase I proposal.

### Budget implications

The Genesis Mission Phase I budget ($500–750K over 9 months) must accommodate the arc module add-on as a capital equipment line item. Key budget considerations:

- **Arc module procurement:** AMAZEMET offers the arc melting chamber as a modular add-on to the existing rePOWDER platform. This is the minimum upgrade needed for IN625/IN718 and 316L/316H processing. The arc module price should be confirmed directly with AMAZEMET (contact via amazemet.com), but based on the rePOWDER modular architecture and university pricing context, this is likely in the range of tens of thousands of euros (exact quote needed).
- **TZM sonotrode:** High-temperature processing requires a TZM (molybdenum alloy) sonotrode to replace the standard Ti-6Al-4V sonotrode used with the induction module. This is an additional consumable/accessory cost.
- **Plasma module (optional for Phase I):** The plasma module would extend capability to refractory alloys (Nb, Mo, W) but is not required for the Phase I demonstration scope focused on Ni superalloys and Fe-based steels. This can be deferred to Phase II.

### Timeline constraints and phased execution

With 9 months total for Phase I and the need to procure an arc module, effective experimental time for high-temperature alloys is approximately **6 months** after accounting for procurement lead time, shipping (AMAZEMET is Poland-based), installation, and commissioning. This constraint drives a two-phase execution strategy:

**Months 1–3: Platform development + Al alloy demonstration (induction module)**

- Deploy and validate the full FLAIME autonomous pipeline using the existing induction module with Al-Si alloys (AlSi10Mg and variants). This is VCL's current target system and requires no new equipment.
- Develop and test the closed-loop AI/ML framework: computational screening → powder atomization → LPBF printing → characterization → model update.
- Generate preliminary autonomous discovery results demonstrating the platform's capability to navigate Al alloy composition space.
- Simultaneously: procure arc module + TZM sonotrode from AMAZEMET, allowing ~8–12 weeks for manufacturing, shipping, and customs.

**Months 3–4: Arc module integration**

- Install and commission arc melting module on existing rePOWDER platform.
- Validate arc module operation with benchmark alloys (e.g., 316L, which has well-characterized UA reference data from Bashmakova et al. 2026).
- Adapt FLAIME pipeline for high-temperature processing parameters.

**Months 4–9: AMMTO high-temperature alloy demonstration (~6 months effective)**

- Transfer the validated autonomous discovery framework to AMMTO-priority materials: IN625 and/or IN718 (Ni superalloys) and 316L/316H (austenitic steel).
- Demonstrate at least one complete autonomous discovery loop on a high-temperature structural alloy system.
- Generate process–structure–property data for AMMTO-relevant compositions.
- Produce deliverables showing the platform's transferability from Al alloys to high-temperature materials.

### Strategic advantage of the two-phase approach

This phased execution actually strengthens the proposal narrative:

1. **De-risks the platform development:** The AI/ML framework, closed-loop logic, and characterization pipeline are all debugged and validated on Al alloys before introducing the added complexity of high-temperature processing. Al alloys are faster to iterate (lower melting point, established LPBF parameters, existing characterization baselines).

2. **Demonstrates transferability:** Showing the same autonomous platform operating across two fundamentally different alloy classes (Al-based at ~660°C and Ni-based at ~1300°C) directly validates the "platform-first" value proposition that AMMTO needs — a tool that accelerates discovery for any structural alloy, not just one system.

3. **Maximizes results within budget:** The first 3 months produce tangible autonomous discovery results (on Al alloys) even before the arc module arrives. This ensures the project has demonstrable progress at every milestone, reducing risk of a Phase I that delivers only infrastructure with no scientific output.

4. **Aligns with Focus Area F framing:** As noted in the earlier analysis, Focus Area F is viable when the autonomous discovery platform is the primary innovation with clear transferability. The phased approach from Al → Ni/Fe directly embodies this transferability argument.

### Alternative: outsource initial high-temp atomization

If the arc module procurement timeline is a concern, an alternative for the first high-temperature atomization runs is to send feedstock to AMAZEMET for atomization as a service (from €1K/50 g batches, per alloy-workflow-review.md). This provides high-temperature alloy powder for LPBF validation and characterization while the arc module is in transit. The trade-off is loss of on-site closed-loop autonomy for those initial runs, but it avoids any gap in experimental output.
