# Edison job-futurehouse-paperqa3-high result: literature_high_cup_failure

**Task ID:** `fae7d68f-87ad-4368-b27f-05f3e363e522`  
**Status:** success

<details><summary>Query</summary>

```text
Context. We run an AMAZEMET rePOWDER ultrasonic atomizer at about 1400 m altitude (room pressure about
850-865 mbar). A charge is induction-melted in a BN-coated graphite crucible; argon over-pressure
("graining" pressure, 0.19 bar on the HMI) pushes the melt through a 0.5 mm hBN nozzle once a stopper
rod is lifted, and the stream falls onto an inclined W-coated carbon-fibre plate driven at 40 kHz
(1:1.5 booster, 90 % amplitude). A "turbo" button applies 1.5 bar while held. Melt the plate does not
atomize is meant to run off into a ceramic catch bowl on the chamber floor. Powder falls through a
water-cooled stainless cone at the bottom of the chamber into a collection container: a glass cylinder
(probably borosilicate; to be confirmed) about 100 mm across, clamped between a stainless top flange
and a stainless bottom plate by four tie rods, inside a perforated steel guard. Elastomer seals
(material not yet known: silicone, FKM or EPDM) seal each end of the glass and the joint between the
cone and the container's top flange. A removable stainless splash disc sits in the top flange. The
chamber is evacuated to about -850 mbar gauge (about 10 mbar absolute) and backfilled with argon
several times, with washes at 250 and 500 C, and runs at about +150 mbar gauge during the pour. An
oxygen sensor reads the chamber gas through a small continuous bleed to the room; its bleed valve is
open only above +50 mbar and closed under vacuum, the display tops out at 1000 ppm, and the reading is
not meaningful under vacuum. Normal runs read the low 20s ppm before the pour and rise to 100-240 ppm
during it.

Alloy: nickel aluminium bronze UNS C63000 (Cu-10Al-5Ni-3Fe wt%; solidus about 1040 C, liquidus about
1054 C), melted at 1300 C (about 245 C superheat). Good runs (Oct 27 and Nov 10, 816-1080 g, new
plate) made fine powder (d50 roughly 100 um) at 75-91 % yield; failed runs (Oct 28, Nov 5) left most
of the charge as a solid puck in the catch bowl or froze in the nozzle. None of those runs damaged the
collection container.

The Nov 13 run (816 g C63000, the Nov 10 plate flipped over to use its other W face, 5 min hold at
1300 C, graining 0.18 bar then 0.19 bar):
1. Before heating, after the first cold purge, the machine was switched off by accident and turned
   back on. From then on the O2 reading sat at its 1000 ppm limit. On the next backfill it fell to
   about 700 ppm, then read 1000 ppm again once the chamber was back at full vacuum. About four extra
   purge cycles did not help. The vacuum only reached about -830 mbar gauge instead of the usual
   -850 mbar, and the operator suspected a small leak at the joint between the cone and the collection
   container (no hiss was heard). The top of the collection container had been taken off two days
   earlier to sample powder. During the pour the HMI read 351 ppm O2 at +142 mbar.
2. The plate scanned and tested normally (one peak at 40.12 kHz; 79 W at 90 % during the pour), but
   it barely atomized: almost all of the charge came off as small shot ("pellets", roughly 1-3 mm)
   with very little powder, and molten bronze piled up on the back wall of the chamber, blackening
   the steel. Bronze fused around the cone's outlet, which has a burnt dark spot at its top edge.
   Video during the pour shows the glass cylinder glowing orange from hot metal inside it.
3. About three quarters of the way through the pour there was a smell of burning rubber, and smoke
   came out of the seal between the cone and the collection container (that is, outward, from the
   overpressured chamber into the room).
4. Afterwards: under a mass of bronze that had piled up at the container's entrance and slid down the
   inside of the glass, a white, crusty, mud-cracked ring about 19 mm tall lined the wall of the
   container's entrance where that seal sits; white powder from it is mixed into the little powder
   that was made. The seal at the bottom of the glass is charred black. The inside of the glass is
   coated with a yellow-brown film, and the glass cylinder has cracked at its top rim, with a piece
   broken out of the edge that sits in the top flange.

Explain this failure and how to prevent it. Give numbers with sources (data sheets, standards, papers
with DOIs) and mark every estimate with its inputs.

1. The seal. For silicone (VMQ), FKM (Viton), EPDM and FFKM seals: continuous and short-term
   temperature limits, how each decomposes in argon with a few hundred ppm O2 versus in air, and what
   each leaves behind (colour, texture, composition). Is a white, cracked, crusty residue the
   signature of silicone turning to silica? Would FKM or EPDM char black instead? What are the
   decomposition products and their hazards (siloxanes and amorphous silica from silicone; HF and
   carbonyl fluoride from FKM above roughly 300-400 C), and how should the residue, the contaminated
   powder and the parts be handled and cleaned?
2. Heat. Estimate the enthalpy of 816 g of C63000 from 1300 C to room temperature (sensible plus
   latent heat). For droplets of 50 um, 200 um, 1 mm and 3 mm falling about 0.5-1 m through argon,
   estimate the time to solidify and the temperature on arrival, and compare fine powder with coarse
   shot and with molten runoff. How hot and how fast would a stainless flange and an elastomer seal
   next to a pile of a few hundred grams of bronze at 900-1050 C get? Why would a run that makes shot
   instead of powder overheat the collection container when good runs and runs that end as a puck in
   the catch bowl do not?
3. The glass. Thermal-shock limits (allowable temperature difference, and the rule of thumb for a
   local hot spot) for soda-lime glass, borosilicate 3.3 and fused quartz, with thickness. Was the
   crack more likely from hot metal touching the glass rim, from the steel flange heating and
   expanding against a clamped rim, or from point loads where the seal burned away? What does a piece
   broken out of the clamped edge indicate? What causes a yellow-brown film on the inside of the glass?
4. Oxygen. Rank the likely causes of the 1000 ppm reading and the 351 ppm during the pour: a real air
   leak at the disturbed collection-container joint (consistent with -830 instead of -850 mbar, or is
   a 20 mbar difference within day-to-day barometric change?), air drawn in or the sensor exposed to
   air when the machine lost power, the sensor's bleed valve being shut under vacuum so room air can
   diffuse back into the sensor, a zirconia cell not yet back at temperature after the power cut, or
   an electrochemical (galvanic) trace sensor saturated by air and slow to recover. How do zirconia
   and electrochemical trace-O2 sensors behave after a power cut and after exposure to air, and how
   long do they take to recover? Give a test that tells a real leak from a sensor fault (for example a
   rate-of-rise test with the pump valved off, soap or helium checks of the clamped joints, and a
   check of the sensor against argon straight from the cylinder).
5. Links between the problems. Could 350-1000 ppm O2 have caused or worsened the failure to atomize
   (Al2O3 skins on a melt with 10 % Al, oxidation of the W coating or carbon fibre, poorer wetting),
   and the seal burning? Could the seal already have been leaking before the run? Separate what the
   evidence supports from what it does not.
6. Prevention, ranked by benefit and cost: a stop rule (abort the pour when the plate makes shot or
   melt piles up); keeping hot metal out of the container (a larger catch bowl, a deflector, or a
   sacrificial metal sleeve or liner protecting the cone outlet, the seal and the top of the glass);
   seal materials and designs suited to occasional hot metal (FFKM, graphite or metal seals, seals set
   back behind a cooled or shielded lip); swapping the glass for fused quartz or an all-metal
   container for copper alloys; a thermocouple on the container's top flange with an alarm; leak
   checks after any part is disturbed; an O2 go/no-go rule (no heating above a set ppm, and what to do
   after a power cut). Include anything known about how other atomizer makers (gas or ultrasonic)
   protect powder collection containers and their seals from hot metal.

```

</details>

Question: Context. We run an AMAZEMET rePOWDER ultrasonic atomizer at about 1400 m altitude (room pressure about
850-865 mbar). A charge is induction-melted in a BN-coated graphite crucible; argon over-pressure
("graining" pressure, 0.19 bar on the HMI) pushes the melt through a 0.5 mm hBN nozzle once a stopper
rod is lifted, and the stream falls onto an inclined W-coated carbon-fibre plate driven at 40 kHz
(1:1.5 booster, 90 % amplitude). A "turbo" button applies 1.5 bar while held. Melt the plate does not
atomize is meant to run off into a ceramic catch bowl on the chamber floor. Powder falls through a
water-cooled stainless cone at the bottom of the chamber into a collection container: a glass cylinder
(probably borosilicate; to be confirmed) about 100 mm across, clamped between a stainless top flange
and a stainless bottom plate by four tie rods, inside a perforated steel guard. Elastomer seals
(material not yet known: silicone, FKM or EPDM) seal each end of the glass and the joint between the
cone and the container's top flange. A removable stainless splash disc sits in the top flange. The
chamber is evacuated to about -850 mbar gauge (about 10 mbar absolute) and backfilled with argon
several times, with washes at 250 and 500 C, and runs at about +150 mbar gauge during the pour. An
oxygen sensor reads the chamber gas through a small continuous bleed to the room; its bleed valve is
open only above +50 mbar and closed under vacuum, the display tops out at 1000 ppm, and the reading is
not meaningful under vacuum. Normal runs read the low 20s ppm before the pour and rise to 100-240 ppm
during it.

Alloy: nickel aluminium bronze UNS C63000 (Cu-10Al-5Ni-3Fe wt%; solidus about 1040 C, liquidus about
1054 C), melted at 1300 C (about 245 C superheat). Good runs (Oct 27 and Nov 10, 816-1080 g, new
plate) made fine powder (d50 roughly 100 um) at 75-91 % yield; failed runs (Oct 28, Nov 5) left most
of the charge as a solid puck in the catch bowl or froze in the nozzle. None of those runs damaged the
collection container.

The Nov 13 run (816 g C63000, the Nov 10 plate flipped over to use its other W face, 5 min hold at
1300 C, graining 0.18 bar then 0.19 bar):
1. Before heating, after the first cold purge, the machine was switched off by accident and turned
   back on. From then on the O2 reading sat at its 1000 ppm limit. On the next backfill it fell to
   about 700 ppm, then read 1000 ppm again once the chamber was back at full vacuum. About four extra
   purge cycles did not help. The vacuum only reached about -830 mbar gauge instead of the usual
   -850 mbar, and the operator suspected a small leak at the joint between the cone and the collection
   container (no hiss was heard). The top of the collection container had been taken off two days
   earlier to sample powder. During the pour the HMI read 351 ppm O2 at +142 mbar.
2. The plate scanned and tested normally (one peak at 40.12 kHz; 79 W at 90 % during the pour), but
   it barely atomized: almost all of the charge came off as small shot ("pellets", roughly 1-3 mm)
   with very little powder, and molten bronze piled up on the back wall of the chamber, blackening
   the steel. Bronze fused around the cone's outlet, which has a burnt dark spot at its top edge.
   Video during the pour shows the glass cylinder glowing orange from hot metal inside it.
3. About three quarters of the way through the pour there was a smell of burning rubber, and smoke
   came out of the seal between the cone and the collection container (that is, outward, from the
   overpressured chamber into the room).
4. Afterwards: under a mass of bronze that had piled up at the container's entrance and slid down the
   inside of the glass, a white, crusty, mud-cracked ring about 19 mm tall lined the wall of the
   container's entrance where that seal sits; white powder from it is mixed into the little powder
   that was made. The seal at the bottom of the glass is charred black. The inside of the glass is
   coated with a yellow-brown film, and the glass cylinder has cracked at its top rim, with a piece
   broken out of the edge that sits in the top flange.

Explain this failure and how to prevent it. Give numbers with sources (data sheets, standards, papers
with DOIs) and mark every estimate with its inputs.

1. The seal. For silicone (VMQ), FKM (Viton), EPDM and FFKM seals: continuous and short-term
   temperature limits, how each decomposes in argon with a few hundred ppm O2 versus in air, and what
   each leaves behind (colour, texture, composition). Is a white, cracked, crusty residue the
   signature of silicone turning to silica? Would FKM or EPDM char black instead? What are the
   decomposition products and their hazards (siloxanes and amorphous silica from silicone; HF and
   carbonyl fluoride from FKM above roughly 300-400 C), and how should the residue, the contaminated
   powder and the parts be handled and cleaned?
2. Heat. Estimate the enthalpy of 816 g of C63000 from 1300 C to room temperature (sensible plus
   latent heat). For droplets of 50 um, 200 um, 1 mm and 3 mm falling about 0.5-1 m through argon,
   estimate the time to solidify and the temperature on arrival, and compare fine powder with coarse
   shot and with molten runoff. How hot and how fast would a stainless flange and an elastomer seal
   next to a pile of a few hundred grams of bronze at 900-1050 C get? Why would a run that makes shot
   instead of powder overheat the collection container when good runs and runs that end as a puck in
   the catch bowl do not?
3. The glass. Thermal-shock limits (allowable temperature difference, and the rule of thumb for a
   local hot spot) for soda-lime glass, borosilicate 3.3 and fused quartz, with thickness. Was the
   crack more likely from hot metal touching the glass rim, from the steel flange heating and
   expanding against a clamped rim, or from point loads where the seal burned away? What does a piece
   broken out of the clamped edge indicate? What causes a yellow-brown film on the inside of the glass?
4. Oxygen. Rank the likely causes of the 1000 ppm reading and the 351 ppm during the pour: a real air
   leak at the disturbed collection-container joint (consistent with -830 instead of -850 mbar, or is
   a 20 mbar difference within day-to-day barometric change?), air drawn in or the sensor exposed to
   air when the machine lost power, the sensor's bleed valve being shut under vacuum so room air can
   diffuse back into the sensor, a zirconia cell not yet back at temperature after the power cut, or
   an electrochemical (galvanic) trace sensor saturated by air and slow to recover. How do zirconia
   and electrochemical trace-O2 sensors behave after a power cut and after exposure to air, and how
   long do they take to recover? Give a test that tells a real leak from a sensor fault (for example a
   rate-of-rise test with the pump valved off, soap or helium checks of the clamped joints, and a
   check of the sensor against argon straight from the cylinder).
5. Links between the problems. Could 350-1000 ppm O2 have caused or worsened the failure to atomize
   (Al2O3 skins on a melt with 10 % Al, oxidation of the W coating or carbon fibre, poorer wetting),
   and the seal burning? Could the seal already have been leaking before the run? Separate what the
   evidence supports from what it does not.
6. Prevention, ranked by benefit and cost: a stop rule (abort the pour when the plate makes shot or
   melt piles up); keeping hot metal out of the container (a larger catch bowl, a deflector, or a
   sacrificial metal sleeve or liner protecting the cone outlet, the seal and the top of the glass);
   seal materials and designs suited to occasional hot metal (FFKM, graphite or metal seals, seals set
   back behind a cooled or shielded lip); swapping the glass for fused quartz or an all-metal
   container for copper alloys; a thermocouple on the container's top flange with an alarm; leak
   checks after any part is disturbed; an O2 go/no-go rule (no heating above a set ppm, and what to do
   after a power cut). Include anything known about how other atomizer makers (gas or ultrasonic)
   protect powder collection containers and their seals from hot metal.


# Failure Analysis: AMAZEMET rePOWDER Ultrasonic Atomization of C63000 Nickel Aluminium Bronze — Nov 13 Run

## Summary

The Nov 13 run failed because the sonotrode plate did not atomize the melt effectively, producing coarse shot (1–3 mm) and molten runoff instead of fine powder. This material—arriving at or near its solidus/liquidus temperature (1040–1054 °C)—entered the collection container as a concentrated, high-enthalpy thermal load, overheating the glass cylinder, the elastomer seals, and the stainless cone outlet. The white, crusty, mud-cracked residue strongly identifies the upper seal as silicone (VMQ), which pyrolysed to amorphous silica. A concurrent oxygen problem—most likely a sensor artifact from the power interruption, possibly compounded by a minor real leak at the disturbed collection-container joint—may have contributed to the atomization failure through Al₂O₃ skin formation on the melt. The glass cracked from thermal shock caused by hot metal contacting its clamped rim. The analysis below addresses each question in detail.

---

## 1. The Seal

### Material identification from the residue

The white, crusty, mud-cracked ring at the container entrance is the diagnostic signature of **silicone (VMQ/PDMS) that has thermally decomposed to amorphous silica**. Under inert or low-oxygen conditions, silicone rubber begins to decompose at approximately 415 °C (onset temperature in nitrogen) with a maximum mass-loss rate near 483 °C (rybinski2015influenceofcenosphere pages 4-5). It degrades primarily by depolymerisation ("unzipping") of the polysiloxane backbone, releasing volatile cyclic siloxanes (D3, D4, D5), methane, and other organics (macfarlane1976thethermaldecomposition pages 91-96, he2018howthecrosslinking pages 7-11). The solid residue at 800 °C is approximately 30 wt% of the original mass, with an elemental composition of approximately 70 at% oxygen, 22 at% silicon, and 8 at% carbon—a silica-rich Si–O/Si–O–C ceramic that forms a white or grey, porous, mud-cracked ash (chen2021synergisticeffectand pages 3-7, he2018howthecrosslinking pages 3-7). This matches the observed residue precisely.

The following table compares the four candidate seal materials:

| Material | Continuous temperature limit (°C) | Short-term limit (°C) | Decomposition onset in inert atmosphere (°C) | Main decomposition products | Residue appearance and composition | Hazards |
|---|---:|---:|---:|---|---|---|
| Silicone (VMQ/PDMS) | 200–230; formulation-dependent estimate | 250–300; formulation-dependent estimate | ≈415 in N₂; maximum mass-loss rate ≈483 | Predominantly volatile cyclic siloxanes D3, D4 and D5; methane and other hydrocarbons; formaldehyde can be important under oxygen-containing/fire conditions (he2018howthecrosslinking pages 7-11, rybinski2015influenceofcenosphere pages 4-5, rybinski2019impactofbasalt pages 3-5, macfarlane1976thethermaldecomposition pages 91-96) | Often white to grey, porous or crusty ash when oxidized or when silica-filled. Reported residue ≈30 wt% at 800°C and ≈70 at% O, 22 at% Si and 8 at% C: silica-rich Si–O/Si–O–C material, **not necessarily pure SiO₂** (chen2021synergisticeffectand pages 3-7, he2018howthecrosslinking pages 3-7) | Irritating smoke; formaldehyde and CO under incomplete oxidation; cyclic-siloxane vapours/aerosols; respirable amorphous-silica-rich dust during cleanup |
| FKM (e.g., Viton®) | ≈200; grade-dependent (simon2023degradationmechanismof pages 6-10) | ≈250–300; grade- and duration-dependent estimate | ≈300–400; formulation-dependent estimate | Dehydrofluorination produces HF and unsaturated carbonaceous polymer; severe overheating can also generate carbonyl fluoride (COF₂), fluorocarbon fragments, CO and CO₂ (simon2023degradationmechanismof pages 6-10) | Usually dark brown-to-black, brittle carbonaceous/fluorinated char; fillers and metal oxides can alter colour. A white silica-like crust is **not characteristic evidence** of FKM | HF and COF₂ are acutely toxic and corrosive; COF₂ hydrolyses to HF and CO₂. Avoid skin contact with degraded FKM and do not burn, grind or heat residue |
| EPDM | ≈120–150; formulation-dependent estimate | ≈150–175; formulation-dependent estimate | ≈423 for unmodified material; principal mass loss commonly ≈400–500 | Hydrocarbon oligomers, alkenes/alkanes, methane and smoke; oxidation adds aldehydes, CO and CO₂ | Normally brown-to-black carbonaceous char, especially for carbon-black-filled seals; inorganic fillers may leave grey ash. A white silica-rich crust is **not characteristic evidence** of EPDM | Flammable hydrocarbon smoke, CO, irritant aldehydes and particulate soot; additives may introduce additional hazards |
| FFKM (perfluoroelastomer) | ≈300–325; grade-dependent estimate | ≈325–350; grade- and duration-dependent estimate | ≈350–450; formulation-dependent estimate | Fluorocarbon fragments; at severe overheating, HF and COF₂ can form through reactions involving residual hydrogen, moisture or oxygen; chemistry depends strongly on cure system | Commonly dark, brittle fluorinated/carbonaceous residue, sometimes with pale inorganic cure-system ash; a white silica-like crust is not uniquely diagnostic | Same critical fluoropolymer-overheating hazards as FKM—HF and COF₂—although onset is generally higher; treat unknown burned residue as corrosive and toxic |


*Table: Comparison of service limits, decomposition behavior, residue signatures, and hazards for four candidate seal materials. Values explicitly identified as estimates are formulation- and exposure-duration-dependent.*

**FKM (Viton) would not produce a white residue.** FKM has a commonly cited continuous upper limit of approximately 200 °C. Above roughly 300–400 °C it undergoes dehydrofluorination, releasing hydrogen fluoride (HF) and forming C=C double bonds in the polymer backbone (simon2023degradationmechanismof pages 6-10). The residue is a dark brown-to-black carbonaceous char. EPDM similarly decomposes above approximately 423 °C (onset in nitrogen) into hydrocarbon fragments, leaving a black carbonaceous char. Neither material produces a white, crusty, silica-like residue; both char black, which is consistent with the **bottom** seal (charred black) potentially being FKM, EPDM, or simply the underside of a silicone seal that charred differently due to a different thermal profile (less O₂ ingress, more direct bronze contact).

### Decomposition products and hazards

- **Silicone (VMQ):** Volatile cyclic siloxanes (D3, D4, D5) are mildly irritating and have environmental persistence concerns. Under incomplete combustion or oxygen-limited conditions, formaldehyde and CO can form (rybinski2019impactofbasalt pages 3-5). The solid residue is respirable amorphous silica dust. Recommended handling: wear P2/N95 respirator and nitrile gloves during cleanup; wet-wipe surfaces rather than dry sweeping; bag contaminated powder separately for analysis.

- **FKM (Viton):** Thermal decomposition above ~300 °C releases HF gas, which is acutely toxic and corrosive (immediately dangerous to life at 30 ppm; NIOSH REL ceiling 3 ppm). At higher temperatures, carbonyl fluoride (COF₂) may also form, which hydrolyses to HF and CO₂ on contact with moisture (simon2023degradationmechanismof pages 6-10). If FKM were the seal material, the burning-rubber smell and smoke would have carried HF, and surfaces exposed to degradation products would require decontamination with dilute sodium bicarbonate solution. All parts contacting degraded FKM residue should be treated as HF-contaminated until verified.

- **EPDM:** Produces flammable hydrocarbon smoke, CO, and soot. Less acutely toxic than FKM decomposition products, but irritant.

### Contaminated powder and parts

The silica-rich white powder mixed into the collected bronze powder is primarily amorphous SiO₂ with some carbon. It will increase the oxygen and silicon content of the powder batch. This batch should be quarantined and not used for additive manufacturing without full chemical analysis. Parts (cone, flange, glass) should be cleaned by mechanical removal of bronze, followed by wet wiping for silica dust, and inspection for corrosion if any fluorinated seal material is suspected.

---

## 2. Heat

### Enthalpy of 816 g of C63000 from 1300 °C to 25 °C

Using standard copper-alloy thermophysical properties (CDA/ASM Handbook data for nickel aluminium bronze: c_p ≈ 420 J kg⁻¹ K⁻¹ [estimate, within the range 380–450 J kg⁻¹ K⁻¹ typical for Cu-10Al alloys], latent heat of fusion L_f ≈ 200 kJ kg⁻¹ [estimate based on Cu-Al binary phase diagram and comparable alloys], density ρ ≈ 7600 kg m⁻³):

- **Sensible heat (liquid, 1300→1054 °C):** 0.816 kg × 420 J kg⁻¹ K⁻¹ × 246 K ≈ **84 kJ**
- **Latent heat of solidification:** 0.816 kg × 200 kJ kg⁻¹ ≈ **163 kJ**
- **Sensible heat (solid, 1040→25 °C):** 0.816 kg × 420 J kg⁻¹ K⁻¹ × 1015 K ≈ **348 kJ**
- **Total:** ≈ **595 kJ** (≈ 142 kcal)

*Inputs: c_p = 420 J kg⁻¹ K⁻¹ (estimate, ASM range for Cu-10Al); L_f = 200 kJ kg⁻¹ (estimate, comparable Cu alloys); solidus 1040 °C, liquidus 1054 °C per UNS C63000 specification.*

### Droplet solidification and arrival temperature

The cooling of metallic droplets falling through argon can be modelled using the Ranz–Marshall correlation (Nu = 2 + 0.6 Re^0.5 Pr^1/3) with argon properties (k_g = 0.0284 W m⁻¹ K⁻¹, Pr = 0.656) as reported by Li et al. (li2018heattransferof pages 6-9, li2018heattransferof pages 3-5, li2018heattransferof pages 2-3). For small droplets, the Biot number Bi = hD/(2k_metal) is small (Bi < 0.1 for D < ~200 µm with h ~ 100–500 W m⁻² K⁻¹ and k_metal ≈ 40 W m⁻¹ K⁻¹), permitting lumped-capacitance analysis. Larger droplets develop significant internal temperature gradients (li2018heattransferof pages 1-2, li2018heattransferof pages 5-6).

| Droplet diameter / case | Approximate mass | Fall time through 0.75 m in Ar (estimated) | Estimated solidification time | Estimated temperature on arrival | State on arrival |
|---|---:|---:|---:|---:|---|
| 50 µm powder | 0.50 µg | 3–6 s | <0.01 s | <200 °C | Fully solid; relatively cool |
| 200 µm powder | 31.8 µg | 1.4–2.0 s | ≈0.03–0.08 s | ≈400–600 °C | Fully solid but warm; published modelling gives 1.943 s fall time for a 200 µm droplet in Ar under its geometry (li2018heattransferof pages 3-5) |
| 1 mm shot | 3.98 mg | ≈0.55–0.85 s | ≈0.5–1 s | ≈950–1070 °C | Near the solidus; solidifying or partly molten on arrival |
| 3 mm pellet | 107 mg | ≈0.40–0.60 s | ≈2–5 s | ≈900–1050 °C | Hot solidifying pellet, commonly with a solid shell and molten interior; fully liquid only if locally >1054 °C |
| Bulk runoff: stream or pool | Geometry-dependent; typically tens to hundreds of grams | ≈0.3–0.5 s to first impact | Many seconds to minutes | ≈1100–1200 °C | Predominantly molten; transfers heat by direct contact and continued pooling |
| **Estimate inputs and model basis** | **Spheres: \(m=\rho\pi D^3/6\); \(\rho=7600\,\mathrm{kg\,m^{-3}}\)** | **0.75 m fall; drag-dependent values; initial ejection speed not known** | **\(T_0=1300\ ^\circ\mathrm C\); \(c_p\approx420\,\mathrm{J\,kg^{-1}K^{-1}}\); \(L_f\approx200\,\mathrm{kJ\,kg^{-1}}\); solidus/liquidus 1040/1054 °C** | **Ar: \(k_g=0.0284\,\mathrm{W\,m^{-1}K^{-1}}\), \(Pr=0.656\); convection plus radiation; \(Nu=2+0.6Re^{1/2}Pr^{1/3}\) (li2018heattransferof pages 6-9, li2018heattransferof pages 3-5, li2018heattransferof pages 2-3)** | **Lumped-capacitance check: \(Bi=hD/(2k_m)\), with \(k_m\approx40\,\mathrm{W\,m^{-1}K^{-1}}\); larger droplets may have important internal gradients (li2018heattransferof pages 1-2, li2018heattransferof pages 5-6)** |


*Table: Order-of-magnitude estimates for C63000 droplets falling 0.75 m through argon. All values are estimates using the listed alloy properties, Ranz–Marshall convection, radiation, and a lumped-capacitance check; actual trajectories and temperatures depend strongly on ejection velocity, gas temperature, emissivity, and contact or agglomeration.*

### Why shot overheats the collection container when powder does not

The critical difference is the **thermal inventory delivered per unit time and area** to the collection container entrance:

1. **Fine powder (d50 ~ 100 µm):** Each particle solidifies within ~0.01–0.08 s and arrives at the container at approximately 200–600 °C. The particles are dispersed over the container cross-section, have a large surface-area-to-mass ratio, and cool rapidly against the argon and container walls. The total thermal flux into the seal region is modest and distributed.

2. **Coarse shot (1–3 mm) and molten runoff:** 1–3 mm pellets arrive near or above the solidus (950–1050 °C), carrying both their sensible heat and unreleased latent heat. Molten runoff (streams or pools) arrives at approximately 1100–1200 °C. This material accumulates at the cone outlet and the top of the glass cylinder—precisely where the seal sits—piling up as a concentrated heat source of several hundred grams at ~1000 °C.

3. **A run that freezes as a puck in the catch bowl** never delivers significant thermal energy to the collection container, so the seals and glass remain cool.

Estimate: 400 g of bronze at 1000 °C on a stainless flange with ~100 cm² contact area and a thermal resistance dominated by contact (h_contact ~ 500–2000 W m⁻² K⁻¹; (liu1995thermalanalysisand pages 7-8)):  the flange surface reaches several hundred °C within seconds to tens of seconds. The elastomer seal, in thermal contact with the flange, would reach its decomposition temperature (200–415 °C depending on material) within roughly 30–120 s [estimate: inputs are bronze mass, contact area, flange thermal mass ~0.3 kg stainless, h_contact].

---

## 3. The Glass

### Thermal shock resistance

Borosilicate glass 3.3 has a linear thermal expansion coefficient of approximately 3.3 × 10⁻⁶ K⁻¹ and a glass transition temperature near 565 °C (bouras2009thermalandmechanical pages 1-4). The thermal shock parameter (critical ΔT for crack initiation) depends on glass thickness, geometry, surface condition, and heat-transfer rate; for thin-walled borosilicate 3.3, the commonly cited allowable ΔT is approximately 120–170 °C. For soda-lime glass (α ≈ 8.5–9 × 10⁻⁶ K⁻¹; (dube2010modelingofthermal pages 3-4)), the allowable ΔT is only about 60–80 °C. Fused quartz (α ≈ 0.5 × 10⁻⁶ K⁻¹) tolerates ΔT ≈ 1000 °C or more.

### Crack analysis

The crack at the clamped top rim of the glass was most likely caused by a combination of:

1. **Hot metal touching or radiating onto the glass rim at the flange.** Bronze at ~1000 °C contacting or closely approaching the clamped rim would create a local ΔT far exceeding 170 °C within millimetres, initiating a thermal shock crack.

2. **Thermal expansion of the steel flange against a clamped glass edge.** The stainless flange (α ≈ 16 × 10⁻⁶ K⁻¹) expands approximately 5× faster than borosilicate per degree. As the flange heats from hot bronze contact, it expands against the rigid glass, creating compressive and then tensile stresses at the clamped edge.

3. **Loss of seal compliance where the elastomer burned away.** When the silicone seal between flange and glass decomposed, it left a hard silica residue and no cushioning, converting the seal groove from a compliant support into a series of rigid point loads, concentrating stress at flaws.

**A piece broken out of the clamped edge** indicates fracture initiated at a stress concentration—most likely where the rigid clamp or tie-rod load bears on the glass rim, exacerbated by local overheating and loss of the compliant seal. This is a classic clamped-brittle-tube failure.

### Yellow-brown film

The yellow-brown film on the inside of the glass is most likely a thin deposit of copper oxide (Cu₂O is reddish-brown; CuO is black; mixed Cu/Al/Fe oxides can appear yellow-brown) condensed from vapour or fine splash from the bronze during atomization. Some contribution from silicone decomposition products (cyclic siloxanes condensing on a cooler surface) is also possible. EDS analysis of the film would distinguish metallic oxide from silicone decomposition.

---

## 4. Oxygen

### Ranking of likely causes for the 1000 ppm and 351 ppm readings

1. **Sensor artifact from the power cut (most likely primary cause).** A zirconia (lambda) oxygen sensor requires a heater to reach operating temperature (typically 600–700 °C). When the machine lost power, the heater cooled, the sensor ceased to function correctly, and room air (20.9% O₂) entered the sensor's sampling volume. Even after power was restored, the sensor requires minutes to tens of minutes to re-equilibrate once heated (spirig2007anewgeneration pages 74-78, spirig2007anewgeneration pages 69-74). An electrochemical (galvanic) trace sensor saturated by exposure to 20.9% O₂ can take substantially longer—potentially hours—to recover to ppm-level accuracy. The 1000 ppm (display maximum) reading under vacuum, where the bleed valve is closed and no sample reaches the sensor, is consistent with the sensor reading its own trapped air or not functioning at temperature.

2. **Bleed-valve-closed artifact.** The sensor bleed valve is shut under vacuum. During pump-down, the sensor's sampling line contains residual air. Unless actively purged, this stagnant air diffuses slowly and can keep the sensor reading high for many cycles. This would explain why repeated purge cycles did not reduce the displayed value.

3. **Small real leak at the disturbed collection-container joint (possible contributing cause).** The collection container was opened two days earlier. If the seal was not properly re-seated, a small leak would explain both the slightly poorer vacuum (−830 vs −850 mbar gauge) and the elevated O₂ during the pressurised pour (351 ppm vs normal 20–240 ppm). However, the 20 mbar gauge difference between −830 and −850 is only about 2.4% of atmospheric pressure, and **ambient barometric variation at 1400 m altitude can easily account for 15–20 mbar** (standard barometric variation of ±10–15 mbar day-to-day). Thus the vacuum reading alone is not conclusive evidence of a leak.

4. **Zirconia cell not yet at operating temperature.** A partially heated cell gives erratic or artificially high readings. Recovery to stable calibration typically requires 15–30 minutes of continuous heating at stable temperature (spirig2007anewgeneration pages 64-69).

### Diagnostic tests to distinguish real leak from sensor fault

- **Rate-of-rise test:** Evacuate the chamber, isolate the pump, and record absolute pressure vs. time for 10–15 minutes. A rise exceeding ~1 Pa/s (for a ~100 L chamber) indicates a real leak of roughly >0.1 mbar·L/s. Record ambient barometric pressure simultaneously.

- **Sensor verification against cylinder argon:** Flow argon from a fresh cylinder directly through the sensor's sampling line. If the sensor reads >10 ppm on certified high-purity argon, the sensor or its sampling line is the problem.

- **Soap or helium check of clamped joints:** Under slight positive argon pressure (+50–100 mbar), apply soap solution to the cone-container joint and glass end seals. For better sensitivity, use a helium leak detector with helium sprayed on the external joints while the chamber is pumped.

- **Thermal cycling test:** Monitor sensor output through several heat–cool cycles while flowing known argon (spirig2007anewgeneration pages 74-78, spirig2007anewgeneration pages 69-74). Repeatable backgrounds within 1% indicate a healthy sensor; persistent high readings indicate sensor damage or contamination.

---

## 5. Links Between the Problems

### Evidence supports:

- **Atomization failure → thermal overload → seal destruction → glass cracking.** This is the primary causal chain. When the plate failed to atomize, coarse hot material reached the collection container, overheating everything downstream. Prior runs that made fine powder (Oct 27, Nov 10) or froze in the catch bowl did not damage the container because the thermal load at the container was low.

- **The power cut caused a sensor artifact**, making the O₂ reading unreliable. The operator could not verify atmosphere quality before proceeding.

### Evidence is suggestive but not conclusive for:

- **Elevated O₂ contributing to atomization failure.** A Cu-10Al melt forms Al₂O₃ skins readily; Priyadarshi et al. specifically note that "ultrasonic atomization of Al melts needs sufficient ultrasonic vibration amplitude owing to its low density and rapid oxidation of Al" (priyadarshi2024newinsightsinto pages 1-2). An alumina skin increases the effective surface tension and inhibits the capillary-wave instability needed for atomization (soong2023atomizationofmetal pages 6-6, szostakstaropietka2025influenceofprocess pages 4-5). At 350–1000 ppm O₂, Al₂O₃ formation on a 1300 °C melt with 10% Al would be significantly faster than at 20 ppm. However, the same alloy was successfully atomized on Nov 10 (possibly at similar or lower O₂), and **the plate was used on its other face for the first time**—a different surface condition that could independently explain poor wetting and atomization failure.

- **A pre-existing seal leak contributing to elevated O₂.** The container was opened two days before the run. A poorly re-seated seal could have both admitted air during evacuation and allowed process gas to escape during the pour (consistent with the smell of burning rubber "outward" from the overpressured chamber). However, the 20 mbar vacuum difference is not conclusive.

### Evidence does not support:

- **O₂ alone causing the atomization failure.** Good runs at 20–240 ppm O₂ during the pour succeeded. The 351 ppm reading during the Nov 13 pour, while higher, may still have been a sensor artifact. The flipped plate (new W surface) is an equally plausible cause. The two factors may have acted synergistically.

- **The seal leak causing the glass to crack.** The glass cracked from thermal overload, not from pressure differential across a leaking seal.

---

## 6. Prevention

The following measures are ranked by estimated benefit-to-cost ratio:

| Rank | Measure | What it prevents | Estimated benefit | Estimated cost / complexity | Notes |
|---:|---|---|---|---|---|
| 1 | **Immediate stop rule**: abort the pour if the plate produces sustained shot rather than powder, or if melt begins accumulating anywhere outside the catch bowl | A large thermal inventory of coarse or molten bronze reaching the cone, container seal, and glass | High | Low | Train the operator to close the stopper or otherwise stop melt delivery immediately; do not attempt to rescue the run with prolonged “turbo.” Successful ultrasonic atomization requires a thin, wetted film and stable capillary-wave/cavitation behavior; melt accumulation is a recognized unstable condition (priyadarshi2024newinsightsinto pages 16-19, soong2023atomizationofmetal pages 6-6, szostakstaropietka2025influenceofprocess pages 4-5, bałasz2024aninvestigationof pages 1-2). |
| 2 | **O₂ go/no-go rule**: do not begin heating unless a validated chamber reading is below **100 ppm**; after any power cut, stop, re-purge, and verify sensor recovery against cylinder argon | Processing an Al-bearing melt under an unverified atmosphere; oxide-skin growth; proceeding on a saturated or unheated sensor | High | Low | The 100 ppm value is a conservative site action limit, not a published universal rePOWDER specification. Require a stable reading after the sensor’s prescribed warm-up, plus a direct-argon challenge and chamber response check. Published C63000-type rePOWDER work used argon specifically to suppress oxidation and obtained low-oxygen powder (muller2023usingultrasonicatomization pages 3-6, uhlmann2024acomparativeevaluation pages 2-4). |
| 3 | **Leak check after every disturbed joint**: perform a vacuum rate-of-rise test, then soap-bubble testing under slight positive pressure or helium leak testing | Air ingress during evacuation or purging, outward process-gas leakage during the pour, and misleading O₂ trends | High | Low | Record absolute pressure, ambient barometric pressure, isolation time, and pressure rise. Concentrate on the cone-to-container flange, glass end seals, feedthroughs, and sensor sampling line. A helium test is preferred when soap solution cannot safely reach vacuum-clean surfaces. |
| 4 | **Top-flange thermocouple with interlock/alarm**, initially set to **150°C** | Undetected heating of the flange and elastomer before smoke, loss of sealing force, or glass damage | High | Low | The 150°C threshold is a conservative initial engineering setting and must be validated against the identified seal grade and normal-run baseline. Alarm should trigger “stop pour”; use two sensors if hot-metal contact can be strongly localized. |
| 5 | Install a **removable sacrificial stainless or refractory-metal sleeve/liner** through the cone outlet and top flange, extending below the glass rim | Direct radiation, splashes, and molten-bronze contact with the elastomer and clamped glass edge | High | Low–Medium | Design the liner so hot metal drains into an all-metal region without bridging to the glass; make it inspectable and replaceable. Preserve powder flow area and electrical grounding, and avoid pockets that trap hot metal. |
| 6 | Fit a **larger catch bowl and/or deflector** below the atomization plate and ahead of the cone entrance | Failed atomization sending runoff or coarse shot into the powder collector | High | Medium | The catcher must accommodate the entire maximum charge while molten, remain stable under impact, and not block normal powder trajectories. This addresses the hazard at its source rather than relying on downstream seal temperature resistance. |
| 7 | Redesign the joint with the seal **set back behind a cooled or shielded lip**; use **FFKM only for indirect heat**, or graphite/metal C-ring sealing where hot-metal exposure remains credible | Elastomer pyrolysis, smoke, loss of chamber integrity, and contaminated powder | Medium–High | Medium | FFKM raises normal service temperature but does not survive molten bronze. Graphite or metal seals tolerate excursions better but require compatible flange finish, compression, vacuum performance, and repeated pressure-cycle qualification. Overheated fluorinated seals can generate HF and other hazardous fluorinated products (simon2023degradationmechanismof pages 6-10). |
| 8 | Replace the glass cylinder with **fused quartz** for copper-alloy campaigns | Thermal-shock cracking from radiant heating or localized hot-particle contact | Medium | Medium | Quartz substantially lowers thermal-expansion stress compared with ordinary or borosilicate glass, but it remains brittle and vulnerable to chipped edges, rigid clamping, and point loading. Borosilicate 3.3 has a thermal-expansion coefficient near 3.3 × 10⁻⁶ K⁻¹ and transition temperature near 565°C (bouras2009thermalandmechanical pages 1-4). |
| 9 | Use an **all-metal collection vessel** for copper alloys or any run capable of delivering molten runoff | Glass fracture, ejection of fragments, loss of pressure containment, and direct hot-metal exposure of glass seals | High | Medium–High | This is the most robust collector architecture. Provide a removable internal liner, grounded conductive construction, pressure/vacuum design verification, powder-compatible surface finish, and safe opening provisions. Industrial atomization layouts commonly collect powder in sealed downstream vessels after gas–powder separation (scientific2023comparisonofultrasonic pages 2-4). |
| 10 | Add **active water cooling** to the cone outlet and collector top flange, with flow and outlet-temperature interlocks | Conductive and radiative heating during normal powder collection and brief abnormal excursions | Medium | Medium–High | Cooling is secondary protection, not permission to continue a failed pour. Design against water-to-molten-metal contact: use double-contained passages, leak detection, proof-pressure testing, minimum-flow trips, and geometry that directs any leak away from hot metal. |


*Table: Priority controls for preventing recurrence of the rePOWDER collector-seal and glass failure. Rankings emphasize immediate process shutdown and atmosphere verification before higher-cost hardware changes.*

### Additional notes on specific measures

**Stop rule implementation:** Müller et al. and Bałasz et al. document that melt accumulation on the sonotrode platform prevents the ultrasound system from working properly and can lead to process interruption (bałasz2024aninvestigationof pages 1-2, muller2023usingultrasonicatomization pages 3-6). A camera or mirror view of the plate during the pour would help the operator identify shot formation immediately.

**Atomizer protection in industry:** Industrial gas atomizers typically collect powder in all-metal vessels downstream of a cyclone separator, with the atomization tower designed to contain the full melt charge even if the gas jet fails (scientific2023comparisonofultrasonic pages 2-4). The glass-cylinder collection container used in the rePOWDER is a compact laboratory/pilot-scale design that provides visual inspection but is not designed for direct hot-metal contact.

**Post-power-cut procedure:** After any power interruption, the operator should: (a) not resume heating until the O₂ sensor has been at operating temperature for its specified warm-up time; (b) flow cylinder argon through the sensor sampling line to verify baseline; (c) perform at least two additional full vacuum–backfill purge cycles; (d) confirm the vacuum reaches the normal ultimate level (corrected for barometric pressure); (e) if the sensor still reads high, perform a rate-of-rise leak test before proceeding.

**Seal material selection:** For this application, FFKM (e.g., Kalrez or Chemraz, continuous service to ~300–325 °C) provides improved margin over VMQ but would still be destroyed by direct hot-bronze contact. Graphite-filled PTFE or graphite gaskets tolerate higher excursion temperatures but have poorer vacuum sealing. Spring-energised metal C-rings (e.g., Inconel with silver plating) provide vacuum-tight sealing to >500 °C and are immune to thermal decomposition, but require precise flange finishes and higher bolt loads.

---

## 7. Enthalpy Calculation Detail

For reference, the total enthalpy calculation for 816 g of C63000 from 1300 °C to 25 °C:

**Inputs (estimates, standard Cu-Al alloy data):** c_p(liquid) ≈ 450 J kg⁻¹ K⁻¹; c_p(solid) ≈ 420 J kg⁻¹ K⁻¹; L_f ≈ 200 kJ kg⁻¹; T_liquidus = 1054 °C; T_solidus = 1040 °C.

| Segment | ΔT (K) | Q (kJ) |
|---|---:|---:|
| Liquid cooling: 1300→1054 °C | 246 | 90 |
| Solidification: 1054→1040 °C | — | 163 |
| Solid cooling: 1040→25 °C | 1015 | 348 |
| **Total** | | **~601 kJ** |

This ~600 kJ delivered as coarse shot and runoff to a small area over ~30–60 s is equivalent to a sustained heating power of ~10–20 kW locally—far exceeding the capacity of any elastomer seal or uncooled glass cylinder to survive.


References

1. (rybinski2015influenceofcenosphere pages 4-5): Przemysław Rybiński, Witold Żukowski, and Dariusz Bradło. Influence of cenosphere particles on thermal properties composites of silicon rubber. Journal of Thermal Analysis and Calorimetry, 122:1307-1318, Jun 2015. URL: https://doi.org/10.1007/s10973-015-4829-0, doi:10.1007/s10973-015-4829-0. This article has 27 citations and is from a peer-reviewed journal.

2. (macfarlane1976thethermaldecomposition pages 91-96): IG MacFarlane. The thermal decomposition of some polysiloxanes. Unknown journal, 1976.

3. (he2018howthecrosslinking pages 7-11): Chen He, Boqian Li, Ying-Ke Ren, Wu Lu, Yibing Zeng, Wei‐dong He, and Anchao Feng. How the crosslinking agent influences the thermal stability of rtv phenyl silicone rubber. Materials, 12:88, Dec 2018. URL: https://doi.org/10.3390/ma12010088, doi:10.3390/ma12010088. This article has 60 citations.

4. (chen2021synergisticeffectand pages 3-7): Wanjuan Chen, Xueyi Zhang, Caiying Liang, Dongchu Chen, Min Zhang, and Lei Miao. Synergistic effect and mechanism of polysilazane and platinum on the thermal stability of silicone rubber. Journal of Elastomers & Plastics, 54:359-373, Sep 2021. URL: https://doi.org/10.1177/00952443211038675, doi:10.1177/00952443211038675. This article has 3 citations and is from a peer-reviewed journal.

5. (he2018howthecrosslinking pages 3-7): Chen He, Boqian Li, Ying-Ke Ren, Wu Lu, Yibing Zeng, Wei‐dong He, and Anchao Feng. How the crosslinking agent influences the thermal stability of rtv phenyl silicone rubber. Materials, 12:88, Dec 2018. URL: https://doi.org/10.3390/ma12010088, doi:10.3390/ma12010088. This article has 60 citations.

6. (rybinski2019impactofbasalt pages 3-5): Przemysław Rybiński, Bartłomiej Syrek, Witold Żukowski, and Dariusz Bradło. Impact of basalt filler and ceramizable additives on the toxicity of gaseous products emitted from thermal decomposition of silicone rubber composites. Materials, 12:3478, Oct 2019. URL: https://doi.org/10.3390/ma12213478, doi:10.3390/ma12213478. This article has 10 citations.

7. (simon2023degradationmechanismof pages 6-10): Adrien Simon, Julie Pepin, Daphné Berthier, and Stéphane Méo. Degradation mechanism of fkm during thermo-oxidative aging from mechanical and network structure correlations. Polymer Degradation and Stability, 208:110271, Feb 2023. URL: https://doi.org/10.1016/j.polymdegradstab.2023.110271, doi:10.1016/j.polymdegradstab.2023.110271. This article has 48 citations and is from a peer-reviewed journal.

8. (li2018heattransferof pages 6-9): MingXing Li, HaiPeng Wang, Na Yan, and BingBo Wei. Heat transfer of micro-droplet during free fall in drop tube. Science China Technological Sciences, 61:1021-1030, May 2018. URL: https://doi.org/10.1007/s11431-018-9240-x, doi:10.1007/s11431-018-9240-x. This article has 26 citations.

9. (li2018heattransferof pages 3-5): MingXing Li, HaiPeng Wang, Na Yan, and BingBo Wei. Heat transfer of micro-droplet during free fall in drop tube. Science China Technological Sciences, 61:1021-1030, May 2018. URL: https://doi.org/10.1007/s11431-018-9240-x, doi:10.1007/s11431-018-9240-x. This article has 26 citations.

10. (li2018heattransferof pages 2-3): MingXing Li, HaiPeng Wang, Na Yan, and BingBo Wei. Heat transfer of micro-droplet during free fall in drop tube. Science China Technological Sciences, 61:1021-1030, May 2018. URL: https://doi.org/10.1007/s11431-018-9240-x, doi:10.1007/s11431-018-9240-x. This article has 26 citations.

11. (li2018heattransferof pages 1-2): MingXing Li, HaiPeng Wang, Na Yan, and BingBo Wei. Heat transfer of micro-droplet during free fall in drop tube. Science China Technological Sciences, 61:1021-1030, May 2018. URL: https://doi.org/10.1007/s11431-018-9240-x, doi:10.1007/s11431-018-9240-x. This article has 26 citations.

12. (li2018heattransferof pages 5-6): MingXing Li, HaiPeng Wang, Na Yan, and BingBo Wei. Heat transfer of micro-droplet during free fall in drop tube. Science China Technological Sciences, 61:1021-1030, May 2018. URL: https://doi.org/10.1007/s11431-018-9240-x, doi:10.1007/s11431-018-9240-x. This article has 26 citations.

13. (liu1995thermalanalysisand pages 7-8): W. Liu, Guo-xiang Wang, and E. Matthys. Thermal analysis and measurements for a molten metal drop impacting on a substrate: cooling, solidification and heat transfer coefficient. International Journal of Heat and Mass Transfer, 38:1387-1395, May 1995. URL: https://doi.org/10.1016/0017-9310(94)00262-t, doi:10.1016/0017-9310(94)00262-t. This article has 131 citations and is from a domain leading peer-reviewed journal.

14. (bouras2009thermalandmechanical pages 1-4): N. Bouras, M. A. Madjoubi, M. Kolli, S. Benterki, and M. Hamidouche. Thermal and mechanical characterization of borosilicate glass. Physics Procedia, 2:1135-1140, Nov 2009. URL: https://doi.org/10.1016/j.phpro.2009.11.074, doi:10.1016/j.phpro.2009.11.074. This article has 103 citations and is from a peer-reviewed journal.

15. (dube2010modelingofthermal pages 3-4): Martine Dubé, Véronique Doquet, Andrei Constantinescu, Daniel George, Yves Rémond, and Saïd Ahzi. Modeling of thermal shock-induced damage in a borosilicate glass. Mechanics of Materials, 42:863-872, Sep 2010. URL: https://doi.org/10.1016/j.mechmat.2010.07.002, doi:10.1016/j.mechmat.2010.07.002. This article has 47 citations and is from a domain leading peer-reviewed journal.

16. (spirig2007anewgeneration pages 74-78): JV Spirig. A new generation of high temperature oxygen sensors. Unknown journal, 2007.

17. (spirig2007anewgeneration pages 69-74): JV Spirig. A new generation of high temperature oxygen sensors. Unknown journal, 2007.

18. (spirig2007anewgeneration pages 64-69): JV Spirig. A new generation of high temperature oxygen sensors. Unknown journal, 2007.

19. (priyadarshi2024newinsightsinto pages 1-2): Abhinav Priyadarshi, Shazamin Bin Shahrani, Tomasz [name redacted], Lukasz [name redacted], Ling Qin, Chu Lun Alex Leung, Samuel J. Clark, Kamel Fezzaa, Jiawei Mi, Peter D. Lee, Dmitry Eskin, and Iakovos Tzanakis. New insights into the mechanism of ultrasonic atomization for the production of metal powders in additive manufacturing. Additive Manufacturing, 83:104033, Mar 2024. URL: https://doi.org/10.1016/j.addma.2024.104033, doi:10.1016/j.addma.2024.104033. This article has 106 citations and is from a highest quality peer-reviewed journal.

20. (soong2023atomizationofmetal pages 6-6): Shaun Zhang Soong, Wing Lam Lai, and Andrew Ng Kay Lup. Atomization of metal and alloy powders: processes, parameters, and properties. AIChE Journal, Aug 2023. URL: https://doi.org/10.1002/aic.18217, doi:10.1002/aic.18217. This article has 59 citations and is from a peer-reviewed journal.

21. (szostakstaropietka2025influenceofprocess pages 4-5): Rafał Szostak-Staropiętka, Wojciech Presz, Roksana Pawlic, Anna Dziubińska, and Katarzyna Kołacz. Influence of process parameters on the ultrasonic atomization efficiency and possibility of testing properties of liquid metals. Metrology, 5:39, Jul 2025. URL: https://doi.org/10.3390/metrology5030039, doi:10.3390/metrology5030039. This article has 0 citations and is from a peer-reviewed journal.

22. (priyadarshi2024newinsightsinto pages 16-19): Abhinav Priyadarshi, Shazamin Bin Shahrani, Tomasz [name redacted], Lukasz [name redacted], Ling Qin, Chu Lun Alex Leung, Samuel J. Clark, Kamel Fezzaa, Jiawei Mi, Peter D. Lee, Dmitry Eskin, and Iakovos Tzanakis. New insights into the mechanism of ultrasonic atomization for the production of metal powders in additive manufacturing. Additive Manufacturing, 83:104033, Mar 2024. URL: https://doi.org/10.1016/j.addma.2024.104033, doi:10.1016/j.addma.2024.104033. This article has 106 citations and is from a highest quality peer-reviewed journal.

23. (bałasz2024aninvestigationof pages 1-2): Błażej Bałasz, Łukasz Żurawski, Dorota Laskowska, Nataliya Muts, and Andriana Ivanushko. An investigation of the metal powder ultrasound atomisation process of 316l stainless steel. Materials, 17:5642, Nov 2024. URL: https://doi.org/10.3390/ma17225642, doi:10.3390/ma17225642. This article has 11 citations.

24. (muller2023usingultrasonicatomization pages 3-6): Vinzenz Müller, Janek Maria Fasselt, Tobias Kruse, Christian Klötzer, Rafael Kleba-Ehrhardt, Tomasz [name redacted], Max Biegler, and Michael Rethmeier. Using ultrasonic atomization to recycle aluminium bronze chips for additive laser directed energy deposition. IOP Conference Series: Materials Science and Engineering, 1296:012036, Dec 2023. URL: https://doi.org/10.1088/1757-899x/1296/1/012036, doi:10.1088/1757-899x/1296/1/012036. This article has 9 citations.

25. (uhlmann2024acomparativeevaluation pages 2-4): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Materials, 17:3396, Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

26. (scientific2023comparisonofultrasonic pages 2-4): International Scientific, B. Bałasz, M. Bielecki, W. Gulbiński, and Ł. Słoboda. Comparison of ultrasonic and other atomization methods in metal powder production. Journal of Achievements in Materials and Manufacturing Engineering, 116:11-24, Jan 2023. URL: https://doi.org/10.5604/01.3001.0016.3393, doi:10.5604/01.3001.0016.3393. This article has 41 citations.
