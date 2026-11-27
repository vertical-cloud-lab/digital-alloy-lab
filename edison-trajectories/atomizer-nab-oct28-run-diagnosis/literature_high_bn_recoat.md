# Edison job-futurehouse-paperqa3-high result: literature_high_bn_recoat

**Task ID:** `1c76847d-c023-4862-a7e2-a8d45fa25874`  
**Status:** success

<details><summary>Query</summary>

```text
Context. We run an AMAZEMET rePOWDER ultrasonic atomizer: a charge is induction-melted in a crucible,
argon over-pressure ("graining" pressure) pushes the melt through a bottom nozzle once a stopper
(sealing) rod is lifted, the stream falls onto an inclined plate driven by an ultrasonic sonotrode
(booster plus horn), and melt that the plate does not atomize runs off into a catch crucible below.
A separate "turbo" button applies 1.5 bar to push the melt out (it replaces, rather than adds to, the
graining pressure). Pressures are read on the HMI; whether they are gauge or absolute is unconfirmed.

Alloy: nickel aluminum bronze UNS C63000 ("630 bronze" rod; Cu-10Al-5Ni-3Fe wt%; liquidus ~1054 C;
liquid density ~6.9-7.0 g/cm3; surface tension ~1.1-1.3 N/m). Melt setpoint 1300 C (the module's
hard limit; ~245 C superheat), read by a thermocouple at the crucible. Crucible: graphite (material to
be confirmed) with its interior sprayed with a boron nitride paint; BN stopper rod; hBN nozzle (bore
about 0.5 mm, to be confirmed). Plate: carbon-fiber composite coated with tungsten (the vendor's
W-coated plate for copper alloys). Booster 1:1.5. Argon atmosphere. In training with aluminum, the
vendor's trainer set the plate so that the melt landed on the plate and rolled down about a third of
the plate's length before it atomized.

Run A (27 Oct): new plate, fresh BN coat, new nozzle, 1080 g charge (four rod pieces), O2 24 ppm,
amplitude 90%, graining 0.19 bar, held 2 min after the charge melted. The stream hit right at the
lower (free) end of the plate. The melt kept flowing only while the operator held the turbo (1.5 bar)
for most of the run; ~97% of the charge was collected as powder, with a visible fraction of flakes.
A thin metal skull stayed on the crucible bottom. When it was removed after cooling, BN came away with
it: light grey crescents of BN on the underside of the skull match the bare patches in the crucible's
coat.

Run B (28 Oct): the same plate (second use; it looked fine), the same nozzle (the bore looked clear),
the same crucible with small bare patches where the BN had come off (not recoated), 858 g charge (five
rod pieces), O2 11 ppm, amplitude 90% for the first quarter of the pour, then 100%; graining 0.23 bar
at the start, back to 0.19 bar about halfway; held 1 min after melting. The plate was moved up a little
so that the stream landed farther up the plate rather than at its very end. Result: the melt "really
struggled to atomize"; some powder was made, but most of the charge ended up as a solid puck in the
catch crucible. Changing amplitude and pressure during the pour did not help.

Focus on the boron nitride coating of the crucible (and of the stopper rod and nozzle). Give numbers
with sources (manufacturer data sheets, foundry practice, papers with DOIs) and mark any estimate.

1. Why would a C63000 skull bond to a sprayed BN coat strongly enough to pull the coat off the
   crucible on cooling? Consider the binders in common BN paints and aerosols (aluminum phosphate,
   silicate, B2O3, organic binders), reaction of the Al in the melt with B2O3 or silica in the binder
   (and the wetting this causes), Al2O3 films, thermal contraction mismatch, coat thickness, and
   whether the coat was fully dried and baked before the first melt.
2. Best practice for re-applying BN on a graphite crucible used for copper alloys and aluminum
   bronze: surface preparation (removing loose coating and skull residue; abrading or not; solvent
   cleaning; avoiding water), stripping the whole coat versus patching the bare spots, number of coats,
   target thickness, drying time between coats, the cure or bake schedule (temperature, atmosphere such
   as air, argon or vacuum, and ramp rate), re-baking to drive off absorbed moisture before use, how to
   check coverage and adhesion, and how many melts a coat typically lasts. Include vendor guidance
   with numbers (for example ZYP Coatings BN Lubricoat and Hardcoat, Momentive or Saint-Gobain Combat
   BN paints, Henze BN, 3M) and say which product types suit an aluminum-containing copper melt.
3. What a patched or partly bare coat does to a C63000 melt at 1300 C: wetting of bare graphite by
   Cu-Al melts (Al4C3 formation), carbon pickup, skull adhesion and melt retention, flakes of coating,
   binder or skull entering the melt and lodging in a ~0.5 mm nozzle bore or otherwise disturbing the
   stream, and B, Si or P pickup in the powder. Could the bare patches or coating debris plausibly
   have caused run B's poor atomization, or are they mainly a contamination and crucible-life issue?
4. Avoiding and removing the skull: draining the crucible fully, end-of-pour pressure, crucible shape,
   keeping the crucible hot until drained, and removing a skull without taking the coat with it.
5. Alternatives for aluminum bronze: thicker or hard-coat BN, solid hBN or pyrolytic BN liners,
   alumina, zirconia or magnesia crucibles, and zirconia or yttria washes.
6. A step-by-step recoat, cure and inspection procedure for the next run, with a go/no-go checklist.

```

</details>

Question: Context. We run an AMAZEMET rePOWDER ultrasonic atomizer: a charge is induction-melted in a crucible,
argon over-pressure ("graining" pressure) pushes the melt through a bottom nozzle once a stopper
(sealing) rod is lifted, the stream falls onto an inclined plate driven by an ultrasonic sonotrode
(booster plus horn), and melt that the plate does not atomize runs off into a catch crucible below.
A separate "turbo" button applies 1.5 bar to push the melt out (it replaces, rather than adds to, the
graining pressure). Pressures are read on the HMI; whether they are gauge or absolute is unconfirmed.

Alloy: nickel aluminum bronze UNS C63000 ("630 bronze" rod; Cu-10Al-5Ni-3Fe wt%; liquidus ~1054 C;
liquid density ~6.9-7.0 g/cm3; surface tension ~1.1-1.3 N/m). Melt setpoint 1300 C (the module's
hard limit; ~245 C superheat), read by a thermocouple at the crucible. Crucible: graphite (material to
be confirmed) with its interior sprayed with a boron nitride paint; BN stopper rod; hBN nozzle (bore
about 0.5 mm, to be confirmed). Plate: carbon-fiber composite coated with tungsten (the vendor's
W-coated plate for copper alloys). Booster 1:1.5. Argon atmosphere. In training with aluminum, the
vendor's trainer set the plate so that the melt landed on the plate and rolled down about a third of
the plate's length before it atomized.

Run A (27 Oct): new plate, fresh BN coat, new nozzle, 1080 g charge (four rod pieces), O2 24 ppm,
amplitude 90%, graining 0.19 bar, held 2 min after the charge melted. The stream hit right at the
lower (free) end of the plate. The melt kept flowing only while the operator held the turbo (1.5 bar)
for most of the run; ~97% of the charge was collected as powder, with a visible fraction of flakes.
A thin metal skull stayed on the crucible bottom. When it was removed after cooling, BN came away with
it: light grey crescents of BN on the underside of the skull match the bare patches in the crucible's
coat.

Run B (28 Oct): the same plate (second use; it looked fine), the same nozzle (the bore looked clear),
the same crucible with small bare patches where the BN had come off (not recoated), 858 g charge (five
rod pieces), O2 11 ppm, amplitude 90% for the first quarter of the pour, then 100%; graining 0.23 bar
at the start, back to 0.19 bar about halfway; held 1 min after melting. The plate was moved up a little
so that the stream landed farther up the plate rather than at its very end. Result: the melt "really
struggled to atomize"; some powder was made, but most of the charge ended up as a solid puck in the
catch crucible. Changing amplitude and pressure during the pour did not help.

Focus on the boron nitride coating of the crucible (and of the stopper rod and nozzle). Give numbers
with sources (manufacturer data sheets, foundry practice, papers with DOIs) and mark any estimate.

1. Why would a C63000 skull bond to a sprayed BN coat strongly enough to pull the coat off the
   crucible on cooling? Consider the binders in common BN paints and aerosols (aluminum phosphate,
   silicate, B2O3, organic binders), reaction of the Al in the melt with B2O3 or silica in the binder
   (and the wetting this causes), Al2O3 films, thermal contraction mismatch, coat thickness, and
   whether the coat was fully dried and baked before the first melt.
2. Best practice for re-applying BN on a graphite crucible used for copper alloys and aluminum
   bronze: surface preparation (removing loose coating and skull residue; abrading or not; solvent
   cleaning; avoiding water), stripping the whole coat versus patching the bare spots, number of coats,
   target thickness, drying time between coats, the cure or bake schedule (temperature, atmosphere such
   as air, argon or vacuum, and ramp rate), re-baking to drive off absorbed moisture before use, how to
   check coverage and adhesion, and how many melts a coat typically lasts. Include vendor guidance
   with numbers (for example ZYP Coatings BN Lubricoat and Hardcoat, Momentive or Saint-Gobain Combat
   BN paints, Henze BN, 3M) and say which product types suit an aluminum-containing copper melt.
3. What a patched or partly bare coat does to a C63000 melt at 1300 C: wetting of bare graphite by
   Cu-Al melts (Al4C3 formation), carbon pickup, skull adhesion and melt retention, flakes of coating,
   binder or skull entering the melt and lodging in a ~0.5 mm nozzle bore or otherwise disturbing the
   stream, and B, Si or P pickup in the powder. Could the bare patches or coating debris plausibly
   have caused run B's poor atomization, or are they mainly a contamination and crucible-life issue?
4. Avoiding and removing the skull: draining the crucible fully, end-of-pour pressure, crucible shape,
   keeping the crucible hot until drained, and removing a skull without taking the coat with it.
5. Alternatives for aluminum bronze: thicker or hard-coat BN, solid hBN or pyrolytic BN liners,
   alumina, zirconia or magnesia crucibles, and zirconia or yttria washes.
6. A step-by-step recoat, cure and inspection procedure for the next run, with a go/no-go checklist.



# Boron Nitride Crucible Coating for C63000 Aluminum Bronze Atomization: Failure Analysis and Best Practice

## 1. Why the C63000 Skull Bonded to and Stripped the BN Coating

The coating pull-out observed in Run A results from several interacting mechanisms operating at 1300 °C on the graphite–BN–C63000 system.

**Binder-mediated wetting and reaction.** Common BN paints use one of several binder systems: phosphate-containing binders (which harden at 800–900 °C into a strong but brittle bond), Al₂O₃-based binders (for service above 1000 °C), Al₂O₃–SiO₂ binders (for temperatures below 1000 °C), and clay or organic binders (rudolph2013boronnitriderelease pages 4-7). If the sprayed BN paint contains a B₂O₃-rich phase (a common residual in commercial hBN powders—ESK HDBN2 contains <0.2 wt% B₂O₃ (nicholas1990someobservationson pages 1-2)) or a silicate/silica binder, the 10 wt% Al in C63000 can reduce these oxides via strongly exothermic aluminothermic reactions: 2Al + B₂O₃ → Al₂O₃ + 2B and 4Al + 3SiO₂ → 2Al₂O₃ + 3Si [estimate based on thermodynamic favorability of Al reduction of B₂O₃ and SiO₂]. The in-situ Al₂O₃ product bridges the melt–coating interface, converting a non-wetting BN surface into a wetted, adherent one. Phosphate binders are explicitly identified as unsuitable for high-thermal-expansion substrates such as metals (rudolph2013boronnitriderelease pages 4-7); if such a binder was used on graphite (CTE 2–20 × 10⁻⁶ K⁻¹ (rudolph2013boronnitriderelease pages 1-4)), the brittle phosphate glass may crack during thermal cycling, providing pathways for melt infiltration.

**High-temperature wetting of BN by aluminum.** BN is poorly wetted by molten aluminum at temperatures below approximately 900 °C, with reported contact angles of approximately 160° (rudolph2013boronnitriderelease pages 4-7). However, between 900 and 1000 °C the contact angle decreases substantially, and independent experiments demonstrated "excellent wetting" of BN by aluminum at 1000 °C (nicholas1990someobservationson pages 3-5). Al–BN joints formed at 1000 °C for 15 min exhibited a shear strength of 6.1 ± 2.0 MPa, failing at the metal–ceramic interface (nicholas1990someobservationson pages 3-5). At 1300 °C—well above this transition—the Al in C63000 has significant activity against BN, and the initial non-wetting behavior that protects the coating at lower temperatures is progressively lost. Although C63000 is predominantly copper (which itself does not wet BN), the 10 wt% Al provides ample reactive potential, especially at extended hold times and with binder impurities reducing the barrier.

**Al₂O₃ film effects.** A continuous Al₂O₃ film on the melt surface initially inhibits wetting of ceramics by aluminum; wetting improves once this oxide film is mechanically disrupted or chemically reduced (nicholas1990someobservationson pages 2-3). In the argon atmosphere of the atomizer (O₂ 24 ppm in Run A), the protective alumina skin on the C63000 melt is thin and may be disrupted by induction stirring, allowing the reactive melt to contact the BN/binder layer directly.

**Thermal contraction mismatch.** The linear CTE of solidified C63000 is approximately 16–18 × 10⁻⁶ K⁻¹ [estimate: generic Cu-alloy range], while that of the BN coating is 0.8–7.5 × 10⁻⁶ K⁻¹ and graphite is 2–20 × 10⁻⁶ K⁻¹, both strongly anisotropic (rudolph2013boronnitriderelease pages 1-4). On cooling from 1300 °C to ambient, the metal skull contracts far more than the substrate and coating [estimated differential free contraction ~1–2%], generating large shear and peel stresses at the coating interfaces (kadhim1990lasercladdingof pages 58-60). Where the skull has even a modest bond to the BN—through binder reaction, local wetting, or mechanical interlocking into porous or cracked coating—these stresses can exceed the cohesive strength of the brittle BN layer or the adhesion of the coating to graphite, pulling off crescent-shaped patches.

**Incomplete cure.** If the BN paint was not fully dried and the binder was not properly cured before the first melt, residual moisture or organic carrier can generate gas at temperature, causing local blistering, poor adhesion, and micro-cracking. An incompletely cured binder will be weaker and more susceptible to pull-out.

The table below summarizes the key material properties relevant to this failure:

| Material / role | Linear CTE, 10⁻⁶ K⁻¹ | Wetting behavior relevant to Al-bearing C63000 | Key reactions / failure significance | Key sources |
|---|---:|---|---|---|
| Graphite crucible | 2–20, anisotropic | Pure Al interacts weakly with graphite at 1000–1150 °C; wetting increases sharply above ≈1150 °C. After 5 min at 1200 °C, reported contact angle ≈85°; above 1200 °C, spreading and a thin adherent layer occur. These pure-Al results are a conservative mechanistic analogue, not direct Cu–10Al data. | Al in exposed C63000 can react as `4Al + 3C → Al₄C₃`; Al₄C₃ and carbon-bearing interfacial products increase anchoring and carbon/inclusion risk. The ≈1300 °C melt temperature lies in the strongly reactive range demonstrated for pure Al. | CTE: (rudolph2013boronnitriderelease pages 1-4); wetting and Al₄C₃: (pastukhov2006wettingofgraphite pages 1-4) |
| Hexagonal BN coating | 0.8–7.5, anisotropic | Molten Al contact angle is reported near 160° up to ≈900 °C, then decreases between ≈900 and 1000 °C. Independent experiments found high-temperature wetting and Al–BN bonding by 1000–1150 °C; an Al–BN joint made at 1000 °C for 15 min had shear strength 6.1 ± 2.0 MPa. | BN is normally a non-wetting release layer, but at 1300 °C its protection depends strongly on coating purity, binder chemistry, oxide films, time, and defects. Phosphate binders harden at 800–900 °C into a strong but brittle phase; reaction-assisted wetting can let a skull pull out weak coating or coating–graphite interfaces. | CTE and non-wetting: (rudolph2013boronnitriderelease pages 4-7, rudolph2013boronnitriderelease pages 1-4); high-temperature wetting and bond strength: (nicholas1990someobservationson pages 3-5, rudolph2013boronnitriderelease pages 4-7); binders: (rudolph2013boronnitriderelease pages 4-7) |
| C63000 solidified skull (Cu–10Al–5Ni–3Fe) | ≈16–18 **[estimate; generic Cu-alloy range]** | No direct Al-on-C63000 wetting angle applies because the skull is the melt itself. The relevant interfaces are C63000/BN or, at defects, C63000/graphite. Its 10 wt% Al supplies substantial chemical activity, but direct Cu–Al/BN and Cu–Al/graphite contact-angle data were not located. | On cooling through roughly 1300 °C to ambient, the skull contracts much more than low-CTE BN and many graphite directions. Differential free contraction is approximately 1–2% **[estimate]**, enough to impose shear/peel stress, especially across thick, brittle, incompletely cured, or locally reacted coating. | Generic CTE/mismatch estimate: (kadhim1990lasercladdingof pages 58-60, rudolph2013boronnitriderelease pages 1-4); analogous shrinkage-driven ceramic pull-out: (nicholas1990someobservationson pages 5-6) |
| Aluminum in the alloy (reactive constituent) | ≈23 **[estimate; solid Al near ambient]** | On BN, Al is strongly non-wetting below ≈900 °C but becomes progressively wetting around 900–1000 °C and above. On graphite, the reported angle falls to ≈85° at 1200 °C after 5 min. An intact Al₂O₃ skin can initially inhibit wetting until it ruptures or is reduced/disrupted. | Al can reduce binder oxides—e.g., `2Al + B₂O₃ → Al₂O₃ + 2B` and `4Al + 3SiO₂ → 2Al₂O₃ + 3Si`—and can form Al₄C₃ on exposed graphite. These reactions can replace a release interface with an adherent Al₂O₃/reaction-product bridge and introduce B or Si into the melt. | Oxide-film effect and BN wetting: (nicholas1990someobservationson pages 2-3, rudolph2013boronnitriderelease pages 4-7); graphite wetting/Al₄C₃: (pastukhov2006wettingofgraphite pages 1-4); CTE estimate and mismatch: (kadhim1990lasercladdingof pages 58-60) |


*Table: Comparison of expansion mismatch, wetting, and reaction pathways for the graphite–BN–C63000 system. Estimates and gaps in alloy-specific wetting data are explicitly identified.*

## 2. Best Practice for Re-Applying BN on the Graphite Crucible

**Product selection.** For an aluminum-containing copper melt at 1300 °C, select a high-purity hBN coating (≥95 wt% BN (rudolph2013boronnitriderelease pages 4-7)) with an alumina-based refractory binder rated for service above 1000 °C (rudolph2013boronnitriderelease pages 4-7). Phosphate-containing binders, while common and strong, harden at 800–900 °C into a brittle glass and are explicitly identified as unsuitable for high-thermal-expansion substrates (rudolph2013boronnitriderelease pages 4-7). Silicate and B₂O₃-rich binders should be avoided because Al in the melt can reduce them, creating wetting and contamination. Products such as ZYP Coatings BN Lubricoat (aerosol, organic binder, maximum service temperature typically ~1000 °C) may be adequate for aluminum casting but may not withstand 1300 °C service with a reactive melt without qualification; ZYP's Hardcoat (inorganic binder) or an equivalent high-temperature product should be evaluated. Henze HeBoCoat products and Momentive/Saint-Gobain Combat BN paints with disclosed binder chemistry should be assessed similarly. Water-based carriers are standard; alcohol (ethanol or isopropanol) carriers reduce the initial moisture load and accelerate drying but introduce flammability concerns (rudolph2013boronnitriderelease pages 4-7).

**Surface preparation.** Strip the entire melt-contact surface rather than patching the bare spots from Run A, because the remaining coating has unknown adhesion and possible subsurface binder degradation. Remove the skull gently without levering against the crucible; use wooden or polymer scrapers, not steel. Lightly hand-abrade retained coating with 320–600 grit SiC paper [estimate]. Vacuum thoroughly with a HEPA system. Wipe with reagent-grade isopropanol or acetone on lint-free cloths until no residue transfers. Do not soak graphite in water or use chlorinated solvents.

**Pre-dry.** Bake the bare crucible under dry argon or vacuum: ramp 1–3 °C/min to 120 °C and hold 1–2 h, then to 200–250 °C and hold 1–2 h [estimate]. Cool under dry inert gas to the coating application temperature.

**Application.** Spraying is recommended over brushing for larger surfaces (rudolph2013boronnitriderelease pages 4-7, rudolph2013boronnitriderelease pages 7-8). Rudolph specifies a spray gun with a 1.5 mm nozzle for best results (rudolph2013boronnitriderelease pages 4-7). Apply 2–4 light cross-coats to a warm substrate [estimate: 40–80 °C], flash-drying each coat at 80–120 °C for 30–60 min [estimate]. Target a total dry thickness of 75–100 µm [estimate]; thin layers minimize stored mismatch stress. Rudolph notes that "extremely thin layers … are needed only for a successful application" of BN release coatings (rudolph2013boronnitriderelease pages 7-8). Foundry practice typically recoats between casts (rudolph2013boronnitriderelease pages 7-8).

**Cure.** Follow the coating manufacturer's specified schedule. A provisional generic schedule [estimate]: ramp 1–3 °C/min to 400 °C and hold 1 h for organic burnout, then to 800–900 °C and hold 1 h for inorganic binder cure, then cool at ≤3 °C/min, all under dry argon or vacuum—not air, as graphite oxidizes significantly above ~400 °C (rudolph2013boronnitriderelease pages 1-4).

**Pre-melt moisture bake.** Within 24 h of charging, rebake at 150–200 °C for 1–2 h under dry argon [estimate] to drive off absorbed atmospheric moisture.

**Inspection.** Check 100% of the melt-contact zone under oblique light and 5–10× magnification. No bare graphite, pinholes, cracks, blisters, or loose powder should be visible. Perform a gentle lint-free wipe test and (if the vendor permits) a low-tack tape test on a witness coupon. Measure thickness on the witness coupon.

**Coating life.** A single BN coating on a graphite crucible handling C63000 at 1300 °C should be treated as consumable and inspected after every melt. In aluminum DC casting, recoating of troughs is done between each casting break (rudolph2013boronnitriderelease pages 7-8). For this atomizer, plan to fully recoat after every 1–3 melts [estimate], or immediately if any bare patches, skull adhesion, or nozzle debris are observed.

## 3. Effects of a Patched or Partly Bare Coat on the C63000 Melt at 1300 °C

**Wetting of bare graphite.** At 1300 °C, the 10 wt% Al in C63000 places the system well within the regime where aluminum aggressively wets graphite and forms Al₄C₃. Pure aluminum on graphite at 1200 °C exhibits a contact angle of approximately 85° after 5 minutes, with spreading, foaming, and intensive carbide formation (pastukhov2006wettingofgraphite pages 1-4). The standard Gibbs energy of Al₄C₃ formation is –47.2 kJ per gram-atom of carbon (pastukhov2006wettingofgraphite pages 1-4). At the 1300 °C superheat used here, the reaction rate will be faster and the wetting more aggressive. Carbon solubility in copper is very low—approximately 8 ppm below 800 °C (zare2026onadvancedcasting pages 20-24)—but the Al₄C₃ reaction product is a solid-phase contaminant rather than a dissolved species.

**Skull adhesion and melt retention.** Where the melt contacts bare graphite at 1300 °C, an adherent Al₄C₃/Al₂O₃ reaction layer forms, bonding the skull to the crucible. This is much stronger than the weak BN release interface. A skull that bonds to bare patches but not to adjacent BN-coated areas will, on cooling, concentrate thermal contraction stresses at the BN/bare boundary, propagating coating delamination laterally.

**Contamination risks.** Flakes of BN coating, binder fragments, or Al₄C₃/graphite reaction products entering the melt can lodge in the approximately 0.5 mm nozzle bore, restricting or blocking the melt stream. Even particles smaller than the bore can partially obstruct flow, alter the stream geometry, and degrade atomization. The alloy powder may be contaminated with boron (from BN or binder B₂O₃ reduction), silicon (from silicate binders), phosphorus (from phosphate binders), and carbon (from graphite exposure). Al₄C₃ is particularly problematic because it hydrolyzes in water to produce Al(OH)₃ and methane, so it can degrade during wet-classification or in humid storage.

**Plausibility of the bare patches causing Run B's poor atomization.** This is plausible but not the sole probable cause. The bare patches from Run A were not recoated before Run B. During Run B, melt contacting these bare graphite areas would react to form adherent Al₄C₃/oxide phases that could: (i) increase skull formation and melt retention, reducing the available melt flow rate; (ii) release particulate debris into the melt stream, partially occluding the ~0.5 mm nozzle bore and producing an intermittent, poorly-formed stream; and (iii) alter the wetting behavior of the melt near the nozzle exit, changing stream geometry. However, other factors may also have contributed to Run B's problems: the lower charge mass (858 g vs. 1080 g), shorter hold time (1 min vs. 2 min), possible lower melt temperature due to the shorter hold, and the changing of amplitude and pressure during the pour. The bare patches are best understood as a compounding factor—they increased the probability of nozzle blockage and inconsistent stream formation—rather than purely a contamination or crucible-life issue. They are also a direct contamination concern for powder quality.

## 4. Avoiding and Removing the Skull

**Draining completely.** The most important defense against skull formation is complete drainage. Maintain the melt at or above 1300 °C (the maximum setpoint) throughout the pour. Apply end-of-pour gas pressure promptly when the melt level drops near the nozzle—use the turbo (1.5 bar) for the final seconds to push residual melt through the nozzle rather than allowing it to freeze. Do not reduce temperature or gas pressure prematurely.

**Crucible geometry.** Ideally, the crucible bottom should taper smoothly to the nozzle exit with no flat areas or pockets where melt can pool and freeze outside the flow path. If the crucible has a flat bottom with the nozzle at the center, some residual melt will always remain in the peripheral region. Confirm with the crucible/atomizer vendor whether the crucible geometry is optimized for drainage.

**Keeping the crucible hot.** The induction heating should remain at full power until the crucible is fully drained. Turning off the induction coil before drainage is complete allows the melt to freeze rapidly on the crucible walls. In the AMAZEMET rePOWDER system, the stopper rod lift and gas pressure sequence should be choreographed so that the melt flows continuously from lift to final drain, with no pauses that allow freezing.

**Removing a skull without damaging the coating.** Warm the crucible gently [estimate: 80–150 °C] to relieve some thermal contraction stress between the skull and the coating/graphite. Lift the skull vertically without levering, twisting, or prying against the crucible wall. Use wooden or polymer tools, never steel, to dislodge residual metal. If the skull is strongly adhered, it is better to sacrifice the skull (cut or drill it out cautiously) than to damage the coating or crucible by brute force. In every case, inspect the coating after skull removal and recoat if any bare patches are revealed.

## 5. Alternatives for Aluminum Bronze

**Thicker or hard-coat BN.** A thicker BN layer provides a larger sacrificial barrier but increases stored thermal mismatch stress and the risk of cracking and spalling. "Hard-coat" products (e.g., ZYP Hardcoat or equivalent) use an inorganic binder that creates a more durable, abrasion-resistant film. For 1300 °C service with reactive Al-bearing melts, a hard-coat BN with an alumina-based binder is preferred over a phosphate-bonded product (rudolph2013boronnitriderelease pages 4-7). The trade-off is that a harder coating is more brittle and less forgiving of thermal mismatch.

**Solid hBN or pyrolytic BN (PBN) liners.** A machined hBN crucible liner, or a pyrolytic BN (PBN) crucible or liner, eliminates the binder problem entirely and provides a continuous, high-purity, non-wetting surface. hBN has a thermal expansion of 0.8–7.5 × 10⁻⁶ K⁻¹ (rudolph2013boronnitriderelease pages 1-4), is non-wetting to aluminum melts up to approximately 900 °C (rudolph2013boronnitriderelease pages 4-7), and has excellent lubricity. PBN is even denser and purer. However, solid hBN is mechanically soft (Mohs hardness <1 (rudolph2013boronnitriderelease pages 1-4)), has relatively low bend strength (~45 MPa for HDBN2 grade (nicholas1990someobservationson pages 1-2)), and does not couple directly with an induction coil. It must be used as a liner inside a graphite susceptor crucible. This is the most effective solution for eliminating binder reactions and ensuring consistent release, though it increases consumable cost. The nozzle and stopper rod in the current setup are already solid hBN, confirming the vendor's familiarity with this approach.

**Alumina (Al₂O₃) crucibles.** Dense alumina crucibles are chemically stable in contact with copper melts and do not introduce carbon. However, alumina is wetted by aluminum at temperatures above approximately 900–1000 °C—with lower contact angles than BN at equivalent temperatures (rudolph2013boronnitriderelease pages 4-7)—so alumina is not a non-wetting material for Al-bearing copper alloys at 1300 °C. Additionally, alumina does not couple with electromagnetic induction fields, requiring a graphite or metallic susceptor.

**Zirconia (ZrO₂) crucibles or washes.** Yttria-stabilized zirconia is thermally stable and has higher fracture toughness than alumina, but like alumina it does not couple with induction and may be wetted by Al-containing melts at 1300 °C. Zirconia or yttria wash coats on graphite are an alternative to BN coatings; they do not have the lubricious release properties of BN but may resist binder-mediated wetting better. These must be qualified for thermal cycling stability on graphite substrates.

**Magnesia (MgO) crucibles.** Magnesia is chemically compatible with many non-ferrous melts and is sometimes used for copper alloy melting. However, it is hygroscopic and thermally shock-sensitive, requiring careful handling. It does not couple with induction.

**Recommendation.** For this application, the most robust near-term improvement is to use a machined hBN liner inside the graphite crucible, eliminating the binder problem. If cost or availability precludes this, use a qualified high-purity BN hard-coat paint with an alumina-based (not phosphate, silicate, or B₂O₃-rich) binder, applied and cured under controlled conditions as described in Section 6.

## 6. Step-by-Step Recoat, Cure, and Inspection Procedure

The following procedure is recommended for preparing the crucible for the next C63000 atomization run. Values marked as estimates must be validated against the selected coating and atomizer manufacturers' instructions.

| Step | Operation | Controlled procedure | Acceptance / **GO** criterion | **NO-GO** condition and action |
|---:|---|---|---|---|
| 1 | Confirm materials and product | Verify crucible is graphite; record BN product, lot, carrier, binder, shelf life, and manufacturer instructions. Obtain written compatibility for graphite, C63000, 1300 °C, argon, and induction service. Treat this procedure as subordinate to the atomizer and coating manufacturers’ instructions. | Materials and approved data sheet are identified and traceable. | Unknown crucible, binder, or nozzle material: stop and obtain confirmation before coating. |
| 2 | Select coating chemistry | Prefer high-purity hBN with the least reactive binder available and explicit approval for graphite and Al-bearing copper at 1300 °C. An alumina-based refractory binder is the preferred starting class for >1000 °C; avoid silica/silicate or B₂O₃-rich products where composition purity matters. Phosphate binders harden at 800–900 °C into strong but brittle bonds and are identified for low-expansion ceramics—not high-expansion metal substrates—so use on graphite only with explicit vendor approval (rudolph2013boronnitriderelease pages 4-7). | Vendor approves product, cure, and chemistry; binder composition is disclosed sufficiently to assess Al, B, Si, and P contamination. | Generic BN aerosol or unknown proprietary binder: do not use for the production run; first qualify it on a graphite coupon with a C63000 melt test. |
| 3 | Protect critical features | Remove the hBN nozzle and BN stopper if permitted; otherwise mask the nozzle seat, thermocouple features, sealing faces, threads, and gas passages. Never spray through or into the ≈0.5 mm bore. | All functional surfaces and passages are positively protected and later inspectable. | Any coating, loose powder, or masking residue enters the bore or sealing interface: clean and borescope/gauge it before proceeding. |
| 4 | Remove residual metal | Warm only enough to release the skull **[estimate: 80–150 °C]**. Lift it without levering against the coating. Remove residual metal with wood, polymer, or another softer nonmetallic tool; do not use steel scrapers or impacts. | No visible metal remains; graphite is not gouged or cracked. | Bonded metal requires force or flexing of the crucible: stop; strip locally under magnification rather than prying. |
| 5 | Decide patch versus full strip | Because the Run-A coating detached in crescents and Run B exposed those areas, fully strip the melt-contact zone to a stable boundary; a complete strip and recoat is preferred for this next diagnostic run. Patch only an isolated defect smaller than about 5 mm with firmly adherent surrounding coating **[estimate]** and only if the same qualified product is used. | Uniform, sound substrate or uniformly adherent retained coat; no feathered, lifted edges. | Multiple bare spots, cracking, blistering, metal undercutting, mixed products, or uncertain cure history: strip the entire melt-contact surface. |
| 6 | Dry-strip loose coating | Vacuum loose material using a HEPA system. Lightly hand-abrade only where needed with clean 320–600 grit SiC paper or a dedicated fine abrasive pad **[estimate]**; use minimal pressure and preserve crucible dimensions. Do not grit-blast unless the crucible vendor authorizes it. | Surface is uniformly matte and free of loose flakes, polished metal smears, and sharp coating steps. | Deep scratches, exposed porosity, dimensional change at the bottom/nozzle seat, or cracks: reject or obtain vendor disposition. |
| 7 | Clean without introducing water | Vacuum again, then wipe with lint-free cloth lightly wetted with reagent-grade IPA or acetone, subject to site safety rules. Use fresh cloths until no grey/metallic residue transfers. Do not soak porous graphite, rinse it with water, use chlorinated cleaner, or touch it with bare hands. Water-based BN systems require forced drying; alcohol carriers reduce the initial water load (rudolph2013boronnitriderelease pages 4-7). | Final cloth is clean; solvent has fully evaporated; no oil, fingerprints, dust, or odor remains. | Persistent contamination or absorbed solvent: repeat cleaning and warm-dry; do not coat a damp or oily crucible. |
| 8 | Pre-dry bare crucible | Bake before coating under flowing dry argon or vacuum: ramp 1–3 °C/min to 120 °C, hold 1–2 h, then to 200–250 °C and hold 1–2 h **[estimate]**. Cool under dry inert gas to the coating manufacturer’s application temperature. Avoid prolonged air heating because graphite oxidizes increasingly above about 400 °C (rudolph2013boronnitriderelease pages 1-4). | No condensate or pressure/outgassing anomaly; mass on a witness coupon is stable **[estimate: <0.1% change over the final hour]**. | Continued outgassing, odor, condensate, or mass loss: extend the hold and investigate contamination. |
| 9 | Prepare coating | Mechanically mix or roll until completely homogeneous; do not entrain foam. Filter only through the mesh specified by the vendor. Adjust viscosity solely with the specified carrier. Prepare a graphite witness coupon alongside the crucible. | No settled agglomerates, skin, gel, or expired material; spray pattern is uniform on a test card. | Lumps, irreversible settling, contamination, or unauthorized dilution: discard the batch. |
| 10 | Apply first coat | Spray rather than brush for uniformity. Rudolph reports a 1.5 mm spray-gun nozzle as suitable (rudolph2013boronnitriderelease pages 4-7). Apply a light mist/tie coat to a warm substrate **[estimate: 40–80 °C]**, rotating the crucible to avoid pools. Keep coating out of the bore and sealing surfaces. | Continuous thin grey-white veil with no runs, pinholes caused by oil, or powder piles. | Runs, mud cracking, fish-eyes, or blocked features: remove the defective wet coat, reclean, and restart. |
| 11 | Flash-dry between coats | Dry each coat at ambient for 10–20 min, then at 80–120 °C for 30–60 min **[estimates; use product data sheet if different]**. Water-based coatings require forced drying (rudolph2013boronnitriderelease pages 4-7). Allow the layer to dry before recoating. | Coat is uniformly matte, non-tacky, and does not mark under a gentle gloved touch on a noncritical rim or witness coupon. | Cool/dark damp areas, bubbling, tackiness, or solvent odor: extend drying; do not trap carrier beneath another coat. |
| 12 | Build final coating | Apply 2–4 light coats **[estimate]**, cross-coating successive passes. Target total dry thickness 50–150 µm **[estimate; initial qualification target: 75–100 µm]**. Keep local variation within approximately ±25 µm **[estimate]**. Thin layers are preferred; overly thick brittle coatings store more mismatch stress. Very thin BN layers can provide release behavior, and foundry applications may be recoated between casts (rudolph2013boronnitriderelease pages 7-8). | Uniform coverage without runs, exposed graphite, thick ridges, or measurable intrusion into fits; witness-coupon thickness is within target. | Less than 50 µm, more than 150 µm, or local accumulations: correct before final cure; if already dry and cracked, strip and restart. |
| 13 | Low-temperature dry | After the final coat, air-dry ≥2 h **[estimate]**, then heat in dry argon or vacuum at 1–2 °C/min to 120 °C and hold 2 h; continue to 250 °C and hold 1–2 h **[estimate]**. Vent water/solvent safely. | No bubbling, blistering, flaking, or sustained outgassing; coating remains uniform. | Any blister or delamination: stop, cool, strip the affected system, and correct surface preparation or coat thickness. |
| 14 | Binder cure | Follow the product-specific cure exactly. If an inorganic coating requires a high-temperature cure, use dry argon or qualified vacuum—not air—above the graphite oxidation range. **Provisional qualification schedule [estimate]:** ramp 1–3 °C/min to 400 °C, hold 1 h; then to 800–900 °C, hold 1 h; cool at ≤3 °C/min under inert gas. Phosphate systems harden at 800–900 °C and become strong but brittle (rudolph2013boronnitriderelease pages 4-7). Do not take an organic-bound aerosol directly into a production melt without its specified burnout cycle. | Witness coupon and crucible show no smoke, odor, bubbles, cracks, or powder shedding; furnace oxygen and exhaust remain within approved limits. | No approved cure schedule, persistent off-gassing, rapid temperature excursion, air leak, or coating damage: no production melt. |
| 15 | Optional service-temperature qualification | Before first production use, qualify the selected coating on a graphite witness coupon—or a sacrificial crucible—through the intended 1300 °C argon cycle. BN’s behavior with Al changes markedly above 900–1000 °C, and Al–BN joints made at 1000 °C for 15 min reached 6.1 ± 2.0 MPa shear strength, so low-temperature appearance alone does not establish release at 1300 °C (rudolph2013boronnitriderelease pages 4-7, nicholas1990someobservationson pages 2-3, nicholas1990someobservationson pages 3-5). | Coupon survives without reaction glazing, spallation, or strong C63000 adhesion; chemistry remains acceptable. | Glazed/wetted areas, strong metal attachment, binder reaction, or flakes: reject that product/schedule and consult the supplier. |
| 16 | Inspect coverage | Under bright oblique light and 5–10× magnification **[estimate]**, inspect 100% of the bottom, wall, transition radii, nozzle seat, and stopper-contact area. Photograph and map the surface. Use UV tracer only if supplied/approved. | No bare graphite, pinholes, cracks, blisters, loose powder, ridges, foreign matter, or coating in excluded areas. | Any defect in the melt-contact zone or near the nozzle: no-go until stripped/repaired and recured. |
| 17 | Check adhesion and thickness | Measure the witness coupon by mass/area or cross-section; use a calibrated eddy-current/ultrasonic method only if validated for BN on graphite. Perform a gentle dry lint-free wipe on the witness and a low-tack tape test only if the coating supplier permits it. Do not score the production crucible. | No flake transfer; only slight pigment transfer if the product is intentionally soft; thickness is within the qualified range. | Flakes, exposed graphite, cohesive chunks, or failed witness adhesion: reject and recoat. |
| 18 | Inspect nozzle and stopper | Clean and inspect the hBN nozzle and BN stopper separately. Pass the manufacturer’s bore gauge or optical measurement through the ≈0.5 mm bore; inspect alignment, chips, deposits, and the sealing line. Apply BN coating to these parts only if their manufacturer specifies it; solid hBN generally should not receive an uncontrolled thick paint layer. | Bore is dimensionally correct and unobstructed; stopper seats uniformly; no loose particles. | Any uncertain bore, crack, chipped edge, coating lump, or poor seal: replace the component. |
| 19 | Final moisture-removal bake | Within 24 h of charging **[estimate]**, rebake assembled compatible parts under dry argon or vacuum: 1–2 °C/min to 150–200 °C, hold 1–2 h **[estimate]**, then keep sealed under dry argon. If storage exceeds 24–48 h or humidity exposure occurs, repeat. | No condensate or abnormal outgassing; system remains dry and protected until charging. | Humidity exposure, cold storage condensation, or unexplained pressure rise: repeat bake and leak check. |
| 20 | Pre-run **GO / NO-GO** release | Record coating product/lot, dry thickness, cure trace, witness result, crucible photos, nozzle bore, stopper seating, argon dew point/O₂, pressure reference (gauge versus absolute), and planned end-of-pour sequence. Reinspect after installation. | **GO only if every preceding criterion passes, the manufacturer approves the coating/cure for graphite and 1300 °C C63000, and the nozzle/stopper are clean and aligned.** | **NO-GO** for any bare graphite, loose coating, unknown binder/cure, dampness, blocked or uncertain bore, damaged hBN, graphite crack, failed witness coupon, or unqualified patch. |
| 21 | Post-run maintenance | Photograph before skull removal. Drain completely while hot using the validated pressure sequence; after cooling, remove residual metal without levering. Inspect and map damage after every melt. Rudolph reports recoating foundry surfaces between casting cycles, though the exact interval must be qualified for this system (rudolph2013boronnitriderelease pages 7-8). | Retain only a fully adherent, defect-free coating within its qualified melt count; record trend data. | Any crescent pull-out, exposed graphite, cracking, contamination, or nozzle debris: retire the coating and fully recoat rather than repeatedly patching it. |


*Table: A controlled recoat, inert-atmosphere cure, inspection, and release procedure for a graphite crucible handling C63000 at 1300 °C. Values labeled as estimates require validation against the selected coating and atomizer manufacturers’ instructions.*

## Summary of Key Findings

The BN coating failure in Run A and the poor atomization in Run B are connected through a cascade of effects: (1) at 1300 °C, the Al in C63000 has significant reactivity toward BN and especially toward binder components (B₂O₃, silicates, phosphates), reducing the non-wetting barrier; (2) thermal contraction mismatch between the high-CTE bronze skull and the low-CTE BN/graphite substrate generates large peel stresses on cooling; (3) the combination of reaction-assisted wetting and contraction stresses pulled crescent-shaped patches of BN off the crucible in Run A; (4) reusing the crucible without recoating in Run B exposed bare graphite to the C63000 melt, promoting Al₄C₃ formation, increased skull adhesion, and particulate debris generation; (5) debris from BN, binder, or reaction products in the melt stream could partially occlude the ~0.5 mm nozzle bore, degrading the stream quality and atomization performance. The remediation strategy focuses on selecting an appropriate binder chemistry, applying a controlled thin coating with proper cure under inert atmosphere, fully stripping and recoating after any coating damage, and qualifying the coating system on a test coupon before production use.


References

1. (rudolph2013boronnitriderelease pages 4-7): Stephan Rudolph. Boron nitride release coatings. ArXiv, pages 163-170, Sep 2013. URL: https://doi.org/10.1002/9781118806364.ch16, doi:10.1002/9781118806364.ch16. This article has 12 citations.

2. (nicholas1990someobservationson pages 1-2): M. G. Nicholas, D. A. Mortimer, L. M. Jones, and R. M. Crispin. Some observations on the wetting and bonding of nitride ceramics. Journal of Materials Science, 25:2679-2689, Jun 1990. URL: https://doi.org/10.1007/bf00584866, doi:10.1007/bf00584866. This article has 218 citations and is from a peer-reviewed journal.

3. (rudolph2013boronnitriderelease pages 1-4): Stephan Rudolph. Boron nitride release coatings. ArXiv, pages 163-170, Sep 2013. URL: https://doi.org/10.1002/9781118806364.ch16, doi:10.1002/9781118806364.ch16. This article has 12 citations.

4. (nicholas1990someobservationson pages 3-5): M. G. Nicholas, D. A. Mortimer, L. M. Jones, and R. M. Crispin. Some observations on the wetting and bonding of nitride ceramics. Journal of Materials Science, 25:2679-2689, Jun 1990. URL: https://doi.org/10.1007/bf00584866, doi:10.1007/bf00584866. This article has 218 citations and is from a peer-reviewed journal.

5. (nicholas1990someobservationson pages 2-3): M. G. Nicholas, D. A. Mortimer, L. M. Jones, and R. M. Crispin. Some observations on the wetting and bonding of nitride ceramics. Journal of Materials Science, 25:2679-2689, Jun 1990. URL: https://doi.org/10.1007/bf00584866, doi:10.1007/bf00584866. This article has 218 citations and is from a peer-reviewed journal.

6. (kadhim1990lasercladdingof pages 58-60): MJ Kadhim. Laser cladding of ceramics and sealing of plasma sprayed zirconia based thermal barrier coatings. Unknown journal, 1990.

7. (pastukhov2006wettingofgraphite pages 1-4): EA Pastukhov, VP Chentsov, and AV Kiselev. Wetting of graphite surface by the aluminium alloys melts. Unknown journal, 2006.

8. (nicholas1990someobservationson pages 5-6): M. G. Nicholas, D. A. Mortimer, L. M. Jones, and R. M. Crispin. Some observations on the wetting and bonding of nitride ceramics. Journal of Materials Science, 25:2679-2689, Jun 1990. URL: https://doi.org/10.1007/bf00584866, doi:10.1007/bf00584866. This article has 218 citations and is from a peer-reviewed journal.

9. (rudolph2013boronnitriderelease pages 7-8): Stephan Rudolph. Boron nitride release coatings. ArXiv, pages 163-170, Sep 2013. URL: https://doi.org/10.1002/9781118806364.ch16, doi:10.1002/9781118806364.ch16. This article has 12 citations.

10. (zare2026onadvancedcasting pages 20-24): Mehran Zare, Kaustubh Kishore Rane, Behzad Niroumand, Omid Ghaderi, Swaroop Kumar Behera, Chanyeop Park, L. G. Salamanca-Riba, and Pradeep K. Rohatgi. On advanced casting methods for synthesis and improvement of microstructural and mechanical properties of graphene reinforced light metal matrix composites. International Journal of Minerals, Metallurgy and Materials, 33:2868-2903, Sep 2026. URL: https://doi.org/10.1007/s12613-026-3388-7, doi:10.1007/s12613-026-3388-7. This article has 5 citations.
